export interface LineupEntry {
  id: number
  user_id: number
  player_id: number
  slot: string
  is_starter: boolean
}

export type LineupPayload = Omit<LineupEntry, 'id' | 'user_id'>
