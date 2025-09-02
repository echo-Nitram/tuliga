import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import RefereesPage from '../app/referees/page';
import '@testing-library/jest-dom';

test('renders referees and adds a new referee', async () => {
  process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000';
  const fetchMock = jest
    .fn()
    .mockResolvedValueOnce({
      ok: true,
      json: async () => [
        { id: 1, name: 'Ref A', level: 'regional' },
      ],
    })
    .mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: 2, name: 'Ref B', level: 'senior' }),
    });

  global.fetch = fetchMock;

  render(<RefereesPage />);

  await waitFor(() => {
    expect(screen.getByText('Ref A - regional')).toBeInTheDocument();
  });
  expect(fetchMock).toHaveBeenCalledWith(
    `${process.env.NEXT_PUBLIC_API_URL}/referees`
  );

  fireEvent.change(screen.getByPlaceholderText('Name'), {
    target: { value: 'Ref B' },
  });
  fireEvent.change(screen.getByDisplayValue('Regional'), {
    target: { value: 'senior' },
  });
  fireEvent.click(screen.getByText('Add'));

  await waitFor(() => {
    expect(screen.getByText('Ref B - senior')).toBeInTheDocument();
  });
  expect(fetchMock).toHaveBeenLastCalledWith(
    `${process.env.NEXT_PUBLIC_API_URL}/referees`,
    expect.objectContaining({ method: 'POST' })
  );

  (global.fetch as jest.Mock).mockRestore?.();
});
