# Ownership: 02 Group Dissolution & Kaiju Cloning

## 1. Dissolution Overview
Group dissolution requires **member consensus**, not unilateral admin action:

- **COUPLE (2 members)**: Both partners must accept the dissolution request. Either member can initiate it, but the other must confirm.
- **FRIENDS (2–6 members)**: A majority vote is required (50 % + 1). The initiator’s vote is cast automatically.

A `dissolution_requests` row is created when a member initiates the process (see `Architecture/05-database-and-auth.md` for the DDL). The request expires in 48 hours if quorum is not reached. Once all required votes are cast, `dissolve_group_and_clone_kaijus()` is executed atomically. Because kaijus are deeply invested entities, they are never deleted — every member receives a clone.

## 2. Kaiju Cloning Protocol
Upon group dissolution, **every member receives an exact clone of every shared kaiju**, placed into their personal `SOLO` group.

### Clone Properties
- **Retained**: Kaiju type, nickname, current stats (hunger, energy, happiness), age, spritesheet data.
- **New**: The clone receives a NEW unique `UUID` and a new `last_interaction_at` timestamp.

## 3. Asset Reconciliation
> [!NOTE]
> Items and customizations are bound to the original purchaser to prevent duplication exploits.

- **Furniture**: Returns to the user who purchased it (`furniture.purchased_by_user_id`). It is placed back in their `SOLO` group's room inventory.
- **Customizations**: Return to the user who set them (`customization.set_by_user_id`). Applied only in their `SOLO` group.
- Members who did not purchase specific furniture or set particular customizations will see default terminal aesthetics upon returning to their solo view.

## 4. Dissolution Sequence
```mermaid
sequenceDiagram
    participant MemberA
    participant API
    participant MemberB
    participant DB Function
    participant Member_Solo_X

    MemberA->>API: POST /groups/{id}/dissolution-request
    API->>API: INSERT dissolution_requests (votes_required=2, votes_cast=1)
    API-->>MemberB: Push notification — dissolution requested
    MemberB->>API: POST /dissolution-requests/{id}/vote (accept)
    API->>API: votes_cast=2 ≥ votes_required=2 → status=ACCEPTED
    API->>DB Function: dissolve_group_and_clone_kaijus(group_id)
    DB Function->>Member_Solo_X: Insert cloned kaijus (New UUIDs) for each member
    DB Function->>Member_Solo_X: Transfer purchased furniture/customizations
    DB Function->>API: DELETE groups CASCADE
    API-->>MemberA: Dissolution Complete
    API-->>MemberB: Dissolution Complete
```

## 5. PostgreSQL Dissolution Function
This function ensures atomic group dissolution, handling the cloning process seamlessly.

```sql
CREATE OR REPLACE FUNCTION dissolve_group_and_clone_kaijus(target_group_id UUID)
RETURNS VOID AS $$
DECLARE
    member_record RECORD;
    kaiju_record RECORD;
    member_solo_group_id UUID;
BEGIN
    -- 1. Loop through every member of the dissolving group
    FOR member_record IN SELECT user_id FROM public.group_members WHERE group_id = target_group_id LOOP
        
        -- Get the member's SOLO group ID
        SELECT id INTO member_solo_group_id FROM public.groups 
        WHERE admin_id = member_record.user_id AND group_type = 'SOLO' LIMIT 1;

        -- 2. Clone every kaiju from the target group into the member's SOLO group
        FOR kaiju_record IN SELECT * FROM public.kaijus WHERE group_id = target_group_id LOOP
            INSERT INTO public.kaijus (
                group_id, kaiju_type, nickname, hunger, energy, happiness, extended_stats, status_flags, age_in_days, last_interaction_at
            ) VALUES (
                member_solo_group_id, 
                kaiju_record.kaiju_type, 
                kaiju_record.nickname, 
                kaiju_record.hunger, 
                kaiju_record.energy, 
                kaiju_record.happiness, 
                kaiju_record.extended_stats,
                kaiju_record.status_flags,
                kaiju_record.age_in_days,
                NOW() -- Fresh interaction timestamp
            );
        END LOOP;
        
        -- 3. Return purchased furniture to the original purchaser's SOLO group
        UPDATE public.furniture_instances
        SET placed_in_group_id = member_solo_group_id
        WHERE purchased_by_user_id = member_record.user_id AND placed_in_group_id = target_group_id;

    END LOOP;

    -- 4. Delete the target group (Cascades to old kaijus, active_group_kaijus, and group_members)
    DELETE FROM public.groups WHERE id = target_group_id;
    
END;
$$ LANGUAGE plpgsql;
```

## 6. Edge Cases
- **Kicked Members**: If a member is involuntarily kicked from a group, the *exact same cloning rules apply*. They receive clones of the kaijus up to the point of their removal, deposited into their `SOLO` group.
