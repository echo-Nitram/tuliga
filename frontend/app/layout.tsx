import './globals.css'
import Navbar from './components/Navbar'

export const metadata = {
  title: 'TuLiga',
  description: 'Gestión de ligas de fútbol amateur en Uruguay',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es">
      <body className="bg-gray-50 text-gray-900 min-h-screen">
        <Navbar />
        <main className="max-w-6xl mx-auto px-4 py-8">
          {children}
        </main>
      </body>
    </html>
  )
}
