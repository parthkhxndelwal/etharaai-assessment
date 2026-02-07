import { BrowserRouter } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import { EmployeeProvider } from './context/EmployeeContext'
import { AttendanceProvider } from './context/AttendanceContext'
import { Toaster } from 'sonner'
import AppRoutes from './routes'

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <EmployeeProvider>
          <AttendanceProvider>
            <AppRoutes />
            <Toaster position="bottom-right" richColors />
          </AttendanceProvider>
        </EmployeeProvider>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
