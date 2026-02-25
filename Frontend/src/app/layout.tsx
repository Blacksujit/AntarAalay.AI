import type { Metadata } from 'next'
import { Inter, Playfair_Display } from 'next/font/google'
import Providers from './providers'
import './globals.css'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })
const playfair = Playfair_Display({ subsets: ['latin'], variable: '--font-playfair' })

export const metadata: Metadata = {
  title: 'AntarAalay.ai - Spatial Intelligence Platform',
  description: 'Design in Harmony. Powered by Intelligence. Ancient Vastu wisdom meets modern AI-driven interior architecture.',
  keywords: ['Vastu', 'AI Interior Design', 'Spatial Intelligence', 'Architecture', 'Harmony'],
  authors: [{ name: 'AntarAalay.ai' }],
  openGraph: {
    title: 'AntarAalay.ai - Spatial Intelligence Platform',
    description: 'Design in Harmony. Powered by Intelligence.',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.variable} ${playfair.variable} font-sans antialiased`}>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  )
}
