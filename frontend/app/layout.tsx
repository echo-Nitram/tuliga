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
      <body>{children}</body>
    </html>
  )
}
