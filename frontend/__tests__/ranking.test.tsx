import { render, screen, waitFor } from '@testing-library/react';
import RankingPage from '../app/ranking';
import '@testing-library/jest-dom';

test('renders ranking fetched from API', async () => {
  process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000';
  global.fetch = jest.fn().mockResolvedValue({
    ok: true,
    json: async () => [
      { team: 'Team A', played: 10, wins: 5, draws: 3, losses: 2, goals_for: 20, goals_against: 10, goal_difference: 10, points: 18 },
      { team: 'Team B', played: 10, wins: 4, draws: 4, losses: 2, goals_for: 15, goals_against: 12, goal_difference: 3, points: 16 },
    ],
  });

  render(<RankingPage />);
  expect(screen.getByText('Ranking')).toBeInTheDocument();

  await waitFor(() => {
    expect(screen.getByText('Team A')).toBeInTheDocument();
    expect(screen.getByText('Team B')).toBeInTheDocument();
  });

  expect(global.fetch).toHaveBeenCalledWith(`${process.env.NEXT_PUBLIC_API_URL}/ranking`);

  (global.fetch as jest.Mock).mockRestore?.();
});
