# Railway cloud validation — 2026-11-21

These checks used isolated projects. Credentials were kept in memory. Test addresses are temporary.

## terraria-cloud

```json
{
  "project_id": "f979fe86-d597-4919-8eab-462db2d33580",
  "service": "Terraria",
  "initial_deployment": {
    "id": "c514f599-b76e-4688-8763-4fd654c05b14",
    "status": "SUCCESS"
  },
  "replacement_deployment": {
    "id": "5f47a8c9-dcd9-456b-b687-f2e16fdf7fb7",
    "status": "SUCCESS"
  },
  "before": {
    "world_id": 402355599,
    "world_name": "Railway",
    "world_guid": "f95015ec-f212-447f-862c-fc8423aea52c",
    "width": 4200,
    "height": 1200,
    "mode": 0,
    "authenticated": true,
    "packet": 7
  },
  "after": {
    "world_id": 402355599,
    "world_name": "Railway",
    "world_guid": "f95015ec-f212-447f-862c-fc8423aea52c",
    "width": 4200,
    "height": 1200,
    "mode": 0,
    "authenticated": true,
    "packet": 7
  },
  "identity_equal": true,
  "same_password_authenticated_after_redeploy": true,
  "scope": "Existing authorized pretest project; no deletion, variable changes or admin setup."
}
```

## terraria-postpublished

```json
{
  "published_template_id": "811452e4-6a80-4c92-b510-282b60a64ff7",
  "published_template_code": "terraria-tshock-server",
  "project_id": "eb859ff6-eccf-4619-8cfa-bcbe1adff38b",
  "deployment": {
    "id": "cf11e1ea-342b-48cf-8d7c-6fc5ec3c5ef1",
    "status": "SUCCESS"
  },
  "wrong_password_rejected_packet_2": true,
  "empty_password_rejected_packet_2": true,
  "correct_password_accepted_world_data_7": true,
  "world": {
    "world_id": 1571980583,
    "world_name": "Railway",
    "world_guid": "d4d9ede9-3a2c-4b40-984f-91353ff94834",
    "width": 4200,
    "height": 1200,
    "mode": 0,
    "authenticated": true,
    "packet": 7
  },
  "pass": true,
  "read_only": true
}
```

