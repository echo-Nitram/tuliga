'use client'

import { useEffect, useState } from 'react'

interface Field {
  id: number
  name: string
  location: string
  price_per_hour: number
}

export default function FieldsPage() {
  const [fields, setFields] = useState<Field[]>([])
  const [provider, setProvider] = useState('stripe')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const baseUrl = process.env.NEXT_PUBLIC_API_URL

  useEffect(() => {
    setLoading(true)
    fetch(`${baseUrl}/fields`)
      .then(res => {
        if (!res.ok) throw new Error(`Error ${res.status}`)
        return res.json()
      })
      .then(setFields)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [baseUrl])

  async function book(fieldId: number) {
    setError(null)
    try {
      const now = new Date()
      const end = new Date(now.getTime() + 60 * 60 * 1000)
      const res = await fetch(`${baseUrl}/fields/${fieldId}/bookings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          start_time: now.toISOString(),
          end_time: end.toISOString(),
          provider
        })
      })
      if (!res.ok) {
        const data = await res.json()
        throw new Error(data.detail || `Error ${res.status}`)
      }
      alert('Reserva confirmada')
    } catch (err: any) {
      setError(err.message)
    }
  }

  if (loading) return <div className="p-4">Cargando canchas...</div>

  return (
    <div>
      <h1 className="text-xl font-bold mb-4">Canchas</h1>
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded mb-4">
          {error}
        </div>
      )}
      <div className="mb-4">
        <label className="mr-2">Proveedor de pago:</label>
        <select value={provider} onChange={e => setProvider(e.target.value)} className="border px-2">
          <option value="stripe">Stripe</option>
          <option value="mercadopago">MercadoPago</option>
        </select>
      </div>
      <ul>
        {fields.map(f => (
          <li key={f.id} className="mb-2">
            <span className="mr-2">{f.name} - {f.location} (${f.price_per_hour}/h)</span>
            <button onClick={() => book(f.id)} className="bg-green-500 text-white px-2">Reservar</button>
          </li>
        ))}
      </ul>
    </div>
  )
}
