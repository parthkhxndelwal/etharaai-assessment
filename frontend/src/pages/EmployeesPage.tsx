import { useEffect, useState } from 'react'
import { useEmployees } from '../context/EmployeeContext'
import { Employee, EmployeeCreate } from '../api/employeeApi'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Label } from '../components/ui/label'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '../components/ui/dialog'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../components/ui/select'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '../components/ui/table'
import { Badge } from '../components/ui/badge'
import { LoadingSpinner } from '../components/LoadingSpinner'
import { ErrorState } from '../components/ErrorState'
import { EmptyState } from '../components/EmptyState'
import { ConfirmDialog } from '../components/ConfirmDialog'
import { toast } from 'sonner'
import { DEPARTMENTS } from '../utils/constants'
import { validateEmail, validateEmployeeId, validateRequired } from '../utils/validators'

export const EmployeesPage = () => {
  const { employees, loading, error, fetchEmployees, addEmployee, removeEmployee } = useEmployees()
  const [searchTerm, setSearchTerm] = useState('')
  const [departmentFilter, setDepartmentFilter] = useState<string>('')
  const [isAddDialogOpen, setIsAddDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [selectedEmployee, setSelectedEmployee] = useState<Employee | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [formData, setFormData] = useState<EmployeeCreate>({
    employee_id: '',
    full_name: '',
    email: '',
    department: '',
    position: '',
  })
  const [formErrors, setFormErrors] = useState<Partial<Record<keyof EmployeeCreate, string>>>({})

  useEffect(() => {
    fetchEmployees()
  }, [fetchEmployees])

  const handleSearch = () => {
    const params: any = {}
    if (searchTerm) params.search = searchTerm
    if (departmentFilter && departmentFilter !== 'all') params.department = departmentFilter
    fetchEmployees(params)
  }

  const handleClearFilters = () => {
    setSearchTerm('')
    setDepartmentFilter('')
    fetchEmployees()
  }

  const validateForm = () => {
    const errors: Partial<Record<keyof EmployeeCreate, string>> = {}
    if (!validateEmployeeId(formData.employee_id)) {
      errors.employee_id = 'Invalid employee ID (use uppercase alphanumeric and hyphens, min 3 chars)'
    }
    if (!validateRequired(formData.full_name)) {
      errors.full_name = 'Full name is required'
    }
    if (!validateEmail(formData.email)) {
      errors.email = 'Invalid email address'
    }
    if (!validateRequired(formData.department)) {
      errors.department = 'Department is required'
    }
    if (!validateRequired(formData.position)) {
      errors.position = 'Position is required'
    }
    setFormErrors(errors)
    return Object.keys(errors).length === 0
  }

  const handleAddEmployee = async () => {
    if (!validateForm()) return

    setIsSubmitting(true)
    try {
      await addEmployee(formData)
      setIsAddDialogOpen(false)
      setFormData({
        employee_id: '',
        full_name: '',
        email: '',
        department: '',
        position: '',
      })
      setFormErrors({})
      toast.success('Employee added successfully')
    } catch (error) {
      toast.error('Failed to add employee', {
        description: error instanceof Error ? error.message : undefined,
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleDeleteEmployee = async () => {
    if (!selectedEmployee) return

    try {
      await removeEmployee(selectedEmployee.employee_id)
      toast.success('Employee deleted successfully')
      setSelectedEmployee(null)
    } catch (error) {
      toast.error('Failed to delete employee', {
        description: error instanceof Error ? error.message : undefined,
      })
    }
  }

  const openViewDialog = (employee: Employee) => {
    setSelectedEmployee(employee)
    setIsViewDialogOpen(true)
  }

  const openDeleteDialog = (employee: Employee) => {
    setSelectedEmployee(employee)
    setIsDeleteDialogOpen(true)
  }

  if (loading && employees.length === 0) {
    return (
      <div className="flex h-full items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (error && employees.length === 0) {
    return <ErrorState message={error} onRetry={() => fetchEmployees()} />
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Employees</h1>
          <p className="text-muted-foreground">Manage your team members</p>
        </div>
        <Button onClick={() => setIsAddDialogOpen(true)}>Add Employee</Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Search & Filter</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-4">
            <div className="flex-1">
              <Input
                placeholder="Search by name or employee ID..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              />
            </div>
            <div className="w-48">
              <Select value={departmentFilter} onValueChange={setDepartmentFilter}>
                <SelectTrigger>
                  <SelectValue placeholder="All Departments" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Departments</SelectItem>
                  {DEPARTMENTS.map((dept) => (
                    <SelectItem key={dept} value={dept}>
                      {dept}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <Button onClick={handleSearch}>Search</Button>
            <Button variant="outline" onClick={handleClearFilters}>
              Clear
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>All Employees ({employees.length})</CardTitle>
        </CardHeader>
        <CardContent>
          {employees.length === 0 ? (
            <EmptyState
              title="No employees found"
              description="Add your first employee to get started"
              action={{ label: 'Add Employee', onClick: () => setIsAddDialogOpen(true) }}
            />
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Employee ID</TableHead>
                  <TableHead>Name</TableHead>
                  <TableHead>Email</TableHead>
                  <TableHead>Department</TableHead>
                  <TableHead>Position</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {employees.map((employee) => (
                  <TableRow key={employee.employee_id}>
                    <TableCell className="font-medium">{employee.employee_id}</TableCell>
                    <TableCell>{employee.full_name}</TableCell>
                    <TableCell>{employee.email}</TableCell>
                    <TableCell>
                      <Badge variant="secondary">{employee.department}</Badge>
                    </TableCell>
                    <TableCell>{employee.position}</TableCell>
                    <TableCell className="text-right">
                      <div className="flex justify-end gap-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => openViewDialog(employee)}
                        >
                          View
                        </Button>
                        <Button
                          size="sm"
                          variant="destructive"
                          onClick={() => openDeleteDialog(employee)}
                        >
                          Delete
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>

      <Dialog open={isAddDialogOpen} onOpenChange={setIsAddDialogOpen}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle>Add New Employee</DialogTitle>
            <DialogDescription>Fill in the employee details below</DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="employee_id">Employee ID</Label>
              <Input
                id="employee_id"
                value={formData.employee_id}
                onChange={(e) =>
                  setFormData({ ...formData, employee_id: e.target.value.toUpperCase() })
                }
                placeholder="EMP-001"
                disabled={isSubmitting}
              />
              {formErrors.employee_id && (
                <p className="text-sm text-destructive">{formErrors.employee_id}</p>
              )}
            </div>
            <div className="space-y-2">
              <Label htmlFor="full_name">Full Name</Label>
              <Input
                id="full_name"
                value={formData.full_name}
                onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                placeholder="John Doe"
                disabled={isSubmitting}
              />
              {formErrors.full_name && (
                <p className="text-sm text-destructive">{formErrors.full_name}</p>
              )}
            </div>
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                placeholder="john@example.com"
                disabled={isSubmitting}
              />
              {formErrors.email && <p className="text-sm text-destructive">{formErrors.email}</p>}
            </div>
            <div className="space-y-2">
              <Label htmlFor="department">Department</Label>
              <Select
                value={formData.department}
                onValueChange={(value) => setFormData({ ...formData, department: value })}
                disabled={isSubmitting}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select department" />
                </SelectTrigger>
                <SelectContent>
                  {DEPARTMENTS.map((dept) => (
                    <SelectItem key={dept} value={dept}>
                      {dept}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {formErrors.department && (
                <p className="text-sm text-destructive">{formErrors.department}</p>
              )}
            </div>
            <div className="space-y-2">
              <Label htmlFor="position">Position</Label>
              <Input
                id="position"
                value={formData.position}
                onChange={(e) => setFormData({ ...formData, position: e.target.value })}
                placeholder="Software Engineer"
                disabled={isSubmitting}
              />
              {formErrors.position && (
                <p className="text-sm text-destructive">{formErrors.position}</p>
              )}
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsAddDialogOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleAddEmployee} disabled={isSubmitting}>
              {isSubmitting ? 'Adding...' : 'Add Employee'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Dialog open={isViewDialogOpen} onOpenChange={setIsViewDialogOpen}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle>Employee Details</DialogTitle>
            <DialogDescription>View complete employee information</DialogDescription>
          </DialogHeader>
          {selectedEmployee && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1">
                  <Label className="text-muted-foreground">Employee ID</Label>
                  <p className="font-medium">{selectedEmployee.employee_id}</p>
                </div>
                <div className="space-y-1">
                  <Label className="text-muted-foreground">Full Name</Label>
                  <p className="font-medium">{selectedEmployee.full_name}</p>
                </div>
              </div>
              <div className="space-y-1">
                <Label className="text-muted-foreground">Email</Label>
                <p className="font-medium">{selectedEmployee.email}</p>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1">
                  <Label className="text-muted-foreground">Department</Label>
                  <Badge variant="secondary">{selectedEmployee.department}</Badge>
                </div>
                <div className="space-y-1">
                  <Label className="text-muted-foreground">Position</Label>
                  <p className="font-medium">{selectedEmployee.position}</p>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1">
                  <Label className="text-muted-foreground">Created At</Label>
                  <p className="text-sm">{new Date(selectedEmployee.created_at).toLocaleString()}</p>
                </div>
                <div className="space-y-1">
                  <Label className="text-muted-foreground">Updated At</Label>
                  <p className="text-sm">{new Date(selectedEmployee.updated_at).toLocaleString()}</p>
                </div>
              </div>
            </div>
          )}
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsViewDialogOpen(false)}>
              Close
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        open={isDeleteDialogOpen}
        onOpenChange={setIsDeleteDialogOpen}
        title="Delete Employee"
        description={`Are you sure you want to delete ${selectedEmployee?.full_name}? This action cannot be undone and will also delete all attendance records.`}
        onConfirm={handleDeleteEmployee}
        confirmLabel="Delete"
        variant="destructive"
      />
    </div>
  )
}
