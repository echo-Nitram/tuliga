'use client';
import { useEffect, useState } from 'react';
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  BarChart,
  Bar,
} from 'recharts';

interface Summary {
  total_teams: number;
  total_players: number;
  total_matches: number;
  avg_goals_per_match: number;
}

interface PlayerStat {
  player: string;
  goals: number;
  assists: number;
}

export default function AdvancedDashboard() {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [players, setPlayers] = useState<PlayerStat[]>([]);

  useEffect(() => {
    fetch('/api/stats/summary')
      .then(res => res.json())
      .then(setSummary);

    fetch('/api/stats/players/top')
      .then(res => res.json())
      .then(setPlayers);
  }, []);

  return (
    <div className="p-4 space-y-8">
      <h1 className="text-2xl font-bold">Advanced Stats</h1>

      {summary && (
        <LineChart width={500} height={300} data={[
          { name: 'Teams', value: summary.total_teams },
          { name: 'Players', value: summary.total_players },
          { name: 'Matches', value: summary.total_matches },
        ]}>
          <CartesianGrid stroke="#ccc" />
          <Line type="monotone" dataKey="value" stroke="#8884d8" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
        </LineChart>
      )}

      {players.length > 0 && (
        <BarChart width={500} height={300} data={players}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="player" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="goals" fill="#82ca9d" />
        </BarChart>
      )}
    </div>
  );
}
