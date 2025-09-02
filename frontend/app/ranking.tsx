'use client';
import { useEffect, useState } from 'react';

interface TeamRow {
  team: string;
  played: number;
  wins: number;
  draws: number;
  losses: number;
  goals_for: number;
  goals_against: number;
  goal_difference: number;
  points: number;
}

export default function RankingPage() {
  const [rows, setRows] = useState<TeamRow[]>([]);

  useEffect(() => {
    const baseUrl = process.env.NEXT_PUBLIC_API_URL;
    fetch(`${baseUrl}/ranking`)
      .then((res) => res.json())
      .then(setRows)
      .catch(console.error);
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Ranking</h1>
      <table className="min-w-full border">
        <thead>
          <tr>
            <th className="border px-2">#</th>
            <th className="border px-2">Team</th>
            <th className="border px-2">Pts</th>
            <th className="border px-2">PJ</th>
            <th className="border px-2">DG</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r, idx) => (
            <tr key={r.team}>
              <td className="border px-2">{idx + 1}</td>
              <td className="border px-2">{r.team}</td>
              <td className="border px-2">{r.points}</td>
              <td className="border px-2">{r.played}</td>
              <td className="border px-2">{r.goal_difference}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
