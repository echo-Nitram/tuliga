import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import FieldsPage from '../app/fields/page';
import '@testing-library/jest-dom';

test('renders fields and books a field', async () => {
  const fetchMock = jest
    .fn()
    .mockResolvedValueOnce({
      ok: true,
      json: async () => [
        { id: 1, name: 'Field A', location: 'City', price_per_hour: 50 },
      ],
    })
    .mockResolvedValueOnce({ ok: true, json: async () => ({}) });

  global.fetch = fetchMock;
  window.alert = jest.fn();

  render(<FieldsPage />);

  await waitFor(() => {
    expect(screen.getByText(/Field A/)).toBeInTheDocument();
  });
  expect(fetchMock).toHaveBeenCalledWith('/api/fields');

  fireEvent.click(screen.getByText('Reservar'));

  await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
  expect(fetchMock).toHaveBeenLastCalledWith(
    '/api/fields/1/bookings',
    expect.objectContaining({ method: 'POST' })
  );
  expect(window.alert).toHaveBeenCalled();

  (global.fetch as jest.Mock).mockRestore?.();
  (window.alert as jest.Mock).mockRestore?.();
});
