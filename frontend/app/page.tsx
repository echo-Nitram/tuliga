import Link from 'next/link'

const features = [
  {
    href: '/tournaments',
    title: 'Torneos',
    description: 'Creá torneos, generá fixtures y seguí los resultados en tiempo real.',
    icon: '🏆',
  },
  {
    href: '/fields',
    title: 'Canchas',
    description: 'Buscá canchas disponibles y reservá tu horario al instante.',
    icon: '🏟️',
  },
  {
    href: '/referees',
    title: 'Árbitros',
    description: 'Gestioná el panel de árbitros y asignalos a cada partido.',
    icon: '🟨',
  },
]

export default function Home() {
  return (
    <div>
      <section className="text-center py-12">
        <h1 className="text-5xl font-extrabold text-emerald-700 mb-4">
          TuLiga
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          La plataforma para organizar ligas de fútbol amateur en Uruguay.
          Torneos, canchas, árbitros — todo en un solo lugar.
        </p>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-4">
        {features.map(f => (
          <Link
            key={f.href}
            href={f.href}
            className="block bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md hover:border-emerald-300 transition-all"
          >
            <div className="text-4xl mb-3">{f.icon}</div>
            <h2 className="text-xl font-bold text-gray-900 mb-2">{f.title}</h2>
            <p className="text-gray-500 text-sm">{f.description}</p>
          </Link>
        ))}
      </section>
    </div>
  )
}
