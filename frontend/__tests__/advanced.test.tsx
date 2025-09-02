import '@testing-library/jest-dom';
import { render, screen, waitFor } from '@testing-library/react';

jest.mock(
  'recharts',
  () => ({
    LineChart: () => null,
    Line: () => null,
    CartesianGrid: () => null,
    XAxis: () => null,
    YAxis: () => null,
    Tooltip: () => null,
    BarChart: () => null,
    Bar: () => null,
  }),
  { virtual: true }
);

import AdvancedDashboard from '../app/dashboard/advanced';

test('fetches stats from configured API', async () => {
  process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000';
  const fetchMock = jest.fn((url: RequestInfo) => {
    if (url === `${process.env.NEXT_PUBLIC_API_URL}/stats/summary`) {
      return Promise.resolve({
        ok: true,
        json: async () => ({
          total_teams: 1,
          total_players: 2,
          total_matches: 3,
          avg_goals_per_match: 1.5,
        }),
      });
    }
    if (url === `${process.env.NEXT_PUBLIC_API_URL}/stats/players/top`) {
      return Promise.resolve({
        ok: true,
        json: async () => [
          { player: 'Alice', goals: 5, assists: 2 },
        ],
      });
    }
    return Promise.reject(new Error('unknown url'));
  });

  global.fetch = fetchMock as any;

  render(<AdvancedDashboard />);
  expect(screen.getByText('Advanced Stats')).toBeInTheDocument();

  await waitFor(() => {
    expect(fetchMock).toHaveBeenCalledWith(
      `${process.env.NEXT_PUBLIC_API_URL}/stats/summary`
    );
    expect(fetchMock).toHaveBeenCalledWith(
      `${process.env.NEXT_PUBLIC_API_URL}/stats/players/top`
    );
  });

  (global.fetch as jest.Mock).mockRestore?.();
});
