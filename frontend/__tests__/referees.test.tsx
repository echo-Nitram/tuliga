import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import RefereesPage from '../app/referees/page';
import '@testing-library/jest-dom';

test('renders referees and adds a new referee', async () => {
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
  expect(fetchMock).toHaveBeenCalledWith('/api/referees');

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
    '/api/referees',
    expect.objectContaining({ method: 'POST' })
  );

  (global.fetch as jest.Mock).mockRestore?.();
});
