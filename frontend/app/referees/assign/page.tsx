'use client'

import { useState } from 'react'

export default function AssignRefereesPage() {
  const [home, setHome] = useState('')
  const [away, setAway] = useState('')
  const [date, setDate] = useState('')
  const [result, setResult] = useState<any>(null)

  async function schedule(e: React.FormEvent) {
    e.preventDefault()
    const res = await fetch('/api/referees/schedule', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify([{ home, away, date }])
    })
    setResult(await res.json())
  }

  return (
    <div>
      <h1 className="text-xl font-bold mb-4">Assign Referees</h1>
      <form onSubmit={schedule} className="space-x-2 mb-4">
        <input value={home} onChange={e => setHome(e.target.value)} placeholder="Home" className="border px-2" />
        <input value={away} onChange={e => setAway(e.target.value)} placeholder="Away" className="border px-2" />
        <input type="date" value={date} onChange={e => setDate(e.target.value)} className="border px-2" />
        <button type="submit" className="bg-green-500 text-white px-2">Schedule</button>
      </form>
      {result && (
        <pre className="bg-gray-100 p-2">{JSON.stringify(result, null, 2)}</pre>
      )}
    </div>
  )
}
