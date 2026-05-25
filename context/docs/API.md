# API Documentation

Base URL in local development:

```txt
http://localhost:8000
```

API prefix:

```txt
/api/v1
```

Frontend API base env variable:

```txt
VITE_API_URL=http://localhost:8000
```

## Health check

### `GET /health`

Returns service status.

Example response:

```json
{
  "status": "ok",
  "service": "gridiron-labs-api"
}
```

## Players API

### `GET /api/v1/players/`

Returns players excluding kickers.

Query parameters:

| Name       |   Type | Required | Description                                                                                  |
| ---------- | -----: | -------: | -------------------------------------------------------------------------------------------- |
| `position` | string |       No | Position filter. Current frontend uses `QB`, `RB`, `WR`, `TE`. Backend uppercases the value. |
| `search`   | string |       No | Case-insensitive player name search.                                                         |

Example:

```txt
GET /api/v1/players/?position=WR&search=jefferson
```

Current response shape:

```ts
type PlayerResponse = {
  id: number;
  sleeper_id: string;
  full_name: string;
  position: string;
  team: string | null;
  status: string;
  gridiron_grade: number;
  matchup_grade: string;
  chaos_score: number;
  opportunity_trend: string;
};
```

Important implementation detail:

- `gridiron_grade`, `matchup_grade`, `chaos_score`, and `opportunity_trend` currently come from deterministic mock grades, not stored database values or live data.

## Roster API

Current routes use `DEV_USER_ID = 1` in the backend. This must be replaced when authentication is implemented.

### `GET /api/v1/roster/`

Returns roster entries for the dev user.

Current response shape is the raw ORM-style roster entry:

```ts
type RosterEntry = {
  id: number;
  user_id: number;
  player_id: number;
};
```

### `POST /api/v1/roster/add/{player_id}`

Adds a player to the dev user's roster.

Path parameters:

| Name        |    Type | Description                    |
| ----------- | ------: | ------------------------------ |
| `player_id` | integer | Database id from `players.id`. |

Success response:

```json
{
  "message": "Player added to roster"
}
```

Known errors:

| Status | Reason                    |
| -----: | ------------------------- |
|    404 | Player not found.         |
|    400 | Player already on roster. |

Note: the current frontend sends a JSON body `{ "playerId": number }`, but the backend only uses the path parameter.

### `DELETE /api/v1/roster/remove/{player_id}`

Removes a player from the dev user's roster.

Success response:

```json
{
  "message": "Player removed from roster"
}
```

Known errors:

| Status | Reason                |
| -----: | --------------------- |
|    404 | Player not on roster. |

## Lineup API

Current routes use `DEV_USER_ID = 1` in the backend. This must be replaced when authentication is implemented.

### `GET /api/v1/lineup/`

Returns lineup entries for the dev user.

Current response shape:

```ts
type LineupEntry = {
  id: number;
  user_id: number;
  player_id: number;
  slot: string;
  is_starter: boolean;
};
```

### `POST /api/v1/lineup/set`

Replaces the dev user's lineup with the submitted list.

Request body:

```ts
type LineupRequest = {
  player_id: number;
  slot: string;
  is_starter: boolean;
};
```

Example:

```json
[
  { "player_id": 1, "slot": "QB", "is_starter": true },
  { "player_id": 2, "slot": "BN", "is_starter": false }
]
```

Success response:

```json
{
  "message": "Lineup updated successfully"
}
```

Known errors:

| Status | Reason                                        |
| -----: | --------------------------------------------- |
|    400 | Submitted player is not on the user's roster. |

Important behavior:

- The endpoint validates every submitted player is already on the roster.
- It deletes the user's existing lineup.
- It inserts the submitted lineup entries.
- This is a full replacement operation, not a patch.

## Recommended API improvements

1. Move request/response types to `backend/app/schemas/`.
2. Return Pydantic response models instead of raw ORM objects.
3. Add route-level response models in FastAPI decorators.
4. Add validation for lineup slots.
5. Add unique constraints to prevent duplicate roster entries and duplicate lineup entries.
6. Replace `DEV_USER_ID` with authenticated user dependency.
7. Add pagination or result limits for `/players/` before production-scale usage.
8. Add consistent error response documentation.
