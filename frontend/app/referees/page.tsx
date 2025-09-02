'use client'

import { useEffect, useState } from 'react'

interface Referee {
  id: number
  name: string
  level: string
}

export default function RefereesPage() {
  const [refs, setRefs] = useState<Referee[]>([])
  const [name, setName] = useState('')
  const [level, setLevel] = useState('regional')
  const baseUrl = process.env.NEXT_PUBLIC_API_URL

  useEffect(() => {
    fetch(`${baseUrl}/referees`)
      .then(res => res.json())
      .then(setRefs)
  }, [baseUrl])

  async function addReferee(e: React.FormEvent) {
    e.preventDefault()
    const res = await fetch(`${baseUrl}/referees`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, level })
    })
    const data = await res.json()
    setRefs([...refs, data])
    setName('')
  }

  return (
    <div>
      <h1 className="text-xl font-bold mb-4">Referees</h1>
      <form onSubmit={addReferee} className="mb-4 space-x-2">
        <input value={name} onChange={e => setName(e.target.value)} placeholder="Name" className="border px-2" />
        <select value={level} onChange={e => setLevel(e.target.value)} className="border px-2">
          <option value="regional">Regional</option>
          <option value="senior">Senior</option>
        </select>
        <button type="submit" className="bg-blue-500 text-white px-2">Add</button>
      </form>
      <ul>
        {refs.map(r => (
          <li key={r.id}>{r.name} - {r.level}</li>
        ))}
      </ul>
    </div>
  )
}
