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

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="text-gray-400 text-lg">Cargando canchas...</div>
      </div>
    )
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Canchas</h1>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
          {error}
        </div>
      )}

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5 mb-8">
        <div className="flex items-center gap-3">
          <label className="text-sm text-gray-500 font-medium">Proveedor de pago:</label>
          <select
            value={provider}
            onChange={e => setProvider(e.target.value)}
            className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
          >
            <option value="stripe">Stripe</option>
            <option value="mercadopago">MercadoPago</option>
          </select>
        </div>
      </div>

      {fields.length === 0 ? (
        <div className="bg-white rounded-xl border border-gray-200 p-8 text-center text-gray-400">
          No hay canchas disponibles
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {fields.map(f => (
            <div key={f.id} className="bg-white rounded-xl border border-gray-200 p-5">
              <h3 className="font-semibold text-gray-900 text-lg mb-1">{f.name}</h3>
              <p className="text-sm text-gray-500 mb-1">{f.location}</p>
              <p className="text-emerald-700 font-bold text-lg mb-3">
                ${f.price_per_hour}<span className="text-sm font-normal text-gray-400">/hora</span>
              </p>
              <button
                onClick={() => book(f.id)}
                className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-2 rounded-lg transition-colors"
              >
                Reservar
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
