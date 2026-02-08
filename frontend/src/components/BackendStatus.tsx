import { useState, useEffect, useCallback, ReactNode } from 'react'
import { API_BASE_URL } from '@/utils/constants'

interface BackendStatusProps {
  children: ReactNode
}

export const BackendStatus = ({ children }: BackendStatusProps) => {
  const [isReady, setIsReady] = useState(false)
  const [dots, setDots] = useState('')

  const checkBackend = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/health`, {
        method: 'GET',
        signal: AbortSignal.timeout(5000),
      })
      if (res.ok) {
        setIsReady(true)
        return true
      }
    } catch {
      // backend not ready yet
    }
    return false
  }, [])

  useEffect(() => {
    let cancelled = false

    const poll = async () => {
      const ok = await checkBackend()
      if (!ok && !cancelled) {
        setTimeout(poll, 3000)
      }
    }

    poll()

    return () => {
      cancelled = true
    }
  }, [checkBackend])

  // Animated dots
  useEffect(() => {
    if (isReady) return
    const interval = setInterval(() => {
      setDots((prev) => (prev.length >= 3 ? '' : prev + '.'))
    }, 500)
    return () => clearInterval(interval)
  }, [isReady])

  if (isReady) return <>{children}</>

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-background px-4">
      <div className="flex flex-col items-center space-y-6 text-center">
        {/* Animated server icon */}
        <div className="relative">
          <div className="h-16 w-16 rounded-full border-4 border-primary/30 border-t-primary animate-spin" />
        </div>

        <div className="space-y-2">
          <h2 className="text-xl font-semibold text-foreground">
            Waking up the server{dots}
          </h2>
          <p className="max-w-sm text-sm text-muted-foreground">
            The backend is hosted on a free tier and may take up to a minute to
            spin up after inactivity. Hang tight!
          </p>
        </div>

        {/* Progress hint */}
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <span className="relative flex h-2 w-2">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-primary opacity-75" />
            <span className="relative inline-flex h-2 w-2 rounded-full bg-primary" />
          </span>
          Connecting to backend
        </div>
      </div>
    </div>
  )
}
