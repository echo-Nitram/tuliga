import Link from 'next/link'

export default function Home() {
  return (
    <main style={{ maxWidth: 800, margin: '0 auto', padding: '2rem' }}>
      <h1>TuLiga</h1>
      <p>Gestión de ligas de fútbol amateur en Uruguay</p>
      <nav>
        <ul>
          <li><Link href="/tournaments">Torneos</Link></li>
          <li><Link href="/fields">Canchas</Link></li>
          <li><Link href="/referees">Árbitros</Link></li>
        </ul>
      </nav>
    </main>
  )
}
