import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import MessagesPage from '../app/messages/page';
import '@testing-library/jest-dom';

test('renders messages for initial conversation', async () => {
  process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000';
  const fetchMock = jest.fn((url: string) => {
    if (url === `${process.env.NEXT_PUBLIC_API_URL}/conversations`) {
      return Promise.resolve({
        ok: true,
        json: async () => [
          { id: 1, title: 'Chat 1' },
          { id: 2, title: 'Chat 2' },
        ],
      });
    }
    if (url === `${process.env.NEXT_PUBLIC_API_URL}/conversations/1/messages`) {
      return Promise.resolve({
        ok: true,
        json: async () => [
          { id: 1, sender: 'Alice', content: 'Hola', timestamp: '' },
          { id: 2, sender: 'Bob', content: 'Qué tal', timestamp: '' },
        ],
      });
    }
    throw new Error(`Unexpected fetch: ${url}`);
  });
  global.fetch = fetchMock as any;

  render(<MessagesPage />);
  expect(screen.getByText('Messages')).toBeInTheDocument();

  await waitFor(() => {
    expect(screen.getByText(/Alice/)).toBeInTheDocument();
    expect(screen.getByText(/Bob/)).toBeInTheDocument();
  });

  expect(fetchMock).toHaveBeenCalledWith(`${process.env.NEXT_PUBLIC_API_URL}/conversations`);
  expect(fetchMock).toHaveBeenCalledWith(
    `${process.env.NEXT_PUBLIC_API_URL}/conversations/1/messages`
  );

  (global.fetch as jest.Mock).mockRestore?.();
});

test('fetches messages for selected conversation', async () => {
  process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000';
  const fetchMock = jest.fn((url: string) => {
    if (url === `${process.env.NEXT_PUBLIC_API_URL}/conversations`) {
      return Promise.resolve({
        ok: true,
        json: async () => [
          { id: 1, title: 'Chat 1' },
          { id: 2, title: 'Chat 2' },
        ],
      });
    }
    if (url === `${process.env.NEXT_PUBLIC_API_URL}/conversations/1/messages`) {
      return Promise.resolve({
        ok: true,
        json: async () => [
          { id: 1, sender: 'Alice', content: 'Hola', timestamp: '' },
        ],
      });
    }
    if (url === `${process.env.NEXT_PUBLIC_API_URL}/conversations/2/messages`) {
      return Promise.resolve({
        ok: true,
        json: async () => [
          { id: 3, sender: 'Carol', content: 'Hi', timestamp: '' },
        ],
      });
    }
    throw new Error(`Unexpected fetch: ${url}`);
  });
  global.fetch = fetchMock as any;

  render(<MessagesPage />);

  await waitFor(() => screen.getByText(/Hola/));

  fireEvent.change(screen.getByLabelText('conversation'), {
    target: { value: '2' },
  });

  await waitFor(() => {
    expect(screen.getByText(/Carol/)).toBeInTheDocument();
  });

  expect(fetchMock).toHaveBeenCalledWith(
    `${process.env.NEXT_PUBLIC_API_URL}/conversations/2/messages`
  );

  (global.fetch as jest.Mock).mockRestore?.();
});
