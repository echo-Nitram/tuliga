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

  useEffect(() => {
    fetch('/api/fields')
      .then(res => res.json())
      .then(setFields)
  }, [])

  async function book(fieldId: number) {
    const now = new Date()
    const end = new Date(now.getTime() + 60 * 60 * 1000)
    await fetch(`/api/fields/${fieldId}/bookings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        start_time: now.toISOString(),
        end_time: end.toISOString(),
        provider
      })
    })
    alert('Reserva confirmada')
  }

  return (
    <div>
      <h1 className="text-xl font-bold mb-4">Canchas</h1>
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
