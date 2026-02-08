import { useAuth } from '@/context/AuthContext'
import { Button } from '@/components/ui/button'
import { getInitials } from '@/utils/formatters'

export const Header = () => {
  const { user, logout } = useAuth()

  return (
    <header className="flex h-16 items-center justify-between border-b bg-card px-6">
      <div className="flex-1" />
      <div className="flex items-center gap-4">
        {user && (
          <>
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary text-sm font-semibold text-primary-foreground">
                {getInitials(user.full_name)}
              </div>
              <div className="text-sm">
                <p className="font-medium">{user.full_name}</p>
                <p className="text-xs text-muted-foreground">{user.email}</p>
              </div>
            </div>
            <Button variant="outline" onClick={logout} size="sm">
              Logout
            </Button>
          </>
        )}
      </div>
    </header>
  )
}
