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
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const baseUrl = process.env.NEXT_PUBLIC_API_URL

  useEffect(() => {
    setLoading(true)
    fetch(`${baseUrl}/referees`)
      .then(res => {
        if (!res.ok) throw new Error(`Error ${res.status}`)
        return res.json()
      })
      .then(setRefs)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [baseUrl])

  async function addReferee(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    try {
      const res = await fetch(`${baseUrl}/referees`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, level })
      })
      if (!res.ok) {
        const data = await res.json()
        throw new Error(data.detail || `Error ${res.status}`)
      }
      const data = await res.json()
      setRefs([...refs, data])
      setName('')
    } catch (err: any) {
      setError(err.message)
    }
  }

  if (loading) return <div className="p-4">Cargando arbitros...</div>

  return (
    <div>
      <h1 className="text-xl font-bold mb-4">Referees</h1>
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded mb-4">
          {error}
        </div>
      )}
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
