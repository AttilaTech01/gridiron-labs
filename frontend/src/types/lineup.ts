export type LineupEntry = {
  id: number;
  user_id: number;
  player_id: number;
  slot: string;
  is_starter: boolean;
};

export type LineupRequest = {
  player_id: number;
  slot: string;
  is_starter: boolean;
};
