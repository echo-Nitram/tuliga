import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom'
import AssignRefereesPage from '../app/referees/assign/page'

test('schedules referees using configured API', async () => {
  process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000'
  const fetchMock = jest.fn().mockResolvedValue({
    ok: true,
    json: async () => ({ success: true })
  })
  global.fetch = fetchMock as any

  render(<AssignRefereesPage />)

  fireEvent.change(screen.getByPlaceholderText('Home'), {
    target: { value: 'Team A' }
  })
  fireEvent.change(screen.getByPlaceholderText('Away'), {
    target: { value: 'Team B' }
  })
  fireEvent.click(screen.getByText('Schedule'))

  await waitFor(() => {
    expect(fetchMock).toHaveBeenCalledWith(
      `${process.env.NEXT_PUBLIC_API_URL}/referees/schedule`,
      expect.objectContaining({ method: 'POST' })
    )
  })

  ;(global.fetch as jest.Mock).mockRestore?.()
})
