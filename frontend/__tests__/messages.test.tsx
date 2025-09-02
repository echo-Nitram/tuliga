import { render, screen, waitFor } from '@testing-library/react';
import MessagesPage from '../app/messages/page';
import '@testing-library/jest-dom';

test('renders messages fetched from API', async () => {
  process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000';
  global.fetch = jest.fn().mockResolvedValue({
    ok: true,
    json: async () => [
      { id: 1, sender: 'Alice', content: 'Hola', timestamp: '' },
      { id: 2, sender: 'Bob', content: 'Qué tal', timestamp: '' },
    ],
  });

  render(<MessagesPage />);
  expect(screen.getByText('Messages')).toBeInTheDocument();

  await waitFor(() => {
    expect(screen.getByText(/Alice/)).toBeInTheDocument();
    expect(screen.getByText(/Bob/)).toBeInTheDocument();
  });

  expect(global.fetch).toHaveBeenCalledWith(`${process.env.NEXT_PUBLIC_API_URL}/conversations/1/messages`);

  (global.fetch as jest.Mock).mockRestore?.();
});
