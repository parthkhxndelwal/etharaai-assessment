import { useEffect, useState } from 'react'
import { useAttendance } from '@/context/AttendanceContext'
import { useEmployees } from '@/context/EmployeeContext'
import { AttendanceCreate } from '@/api/attendanceApi'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'
import { LoadingSpinner } from '@/components/LoadingSpinner'
import { ErrorState } from '@/components/ErrorState'
import { EmptyState } from '@/components/EmptyState'
import { ConfirmDialog } from '@/components/ConfirmDialog'
import { toast } from 'sonner'
import { ATTENDANCE_STATUS } from '@/utils/constants'
import { formatDate, formatDateISO } from '@/utils/formatters'

export const AttendancePage = () => {
  const { records, loading, error, fetchAttendance, markAttendance, removeAttendance } = useAttendance()
  const { employees, fetchEmployees } = useEmployees()
  const [isMarkDialogOpen, setIsMarkDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [selectedRecord, setSelectedRecord] = useState<any>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [filters, setFilters] = useState({
    employee_id: '',
    status: '',
    start_date: '',
    end_date: '',
  })
  const [formData, setFormData] = useState<AttendanceCreate>({
    employee_id: '',
    date: formatDateISO(new Date()),
    status: ATTENDANCE_STATUS.PRESENT,
    notes: '',
  })

  useEffect(() => {
    fetchAttendance()
    fetchEmployees()
  }, [fetchAttendance, fetchEmployees])

  const handleApplyFilters = () => {
    const filterParams: any = {}
    if (filters.employee_id && filters.employee_id !== 'all') filterParams.employee_id = filters.employee_id
    if (filters.status && filters.status !== 'all') filterParams.status = filters.status
    if (filters.start_date) filterParams.start_date = filters.start_date
    if (filters.end_date) filterParams.end_date = filters.end_date
    fetchAttendance(filterParams)
  }

  const handleClearFilters = () => {
    setFilters({ employee_id: '', status: '', start_date: '', end_date: '' })
    fetchAttendance()
  }

  const openDeleteDialog = (record: any) => {
    setSelectedRecord(record)
    setIsDeleteDialogOpen(true)
  }

  const handleDeleteAttendance = async () => {
    if (!selectedRecord) return

    try {
      await removeAttendance(selectedRecord.id)
      toast.success('Attendance record deleted successfully')
      setSelectedRecord(null)
    } catch (error) {
      toast.error('Failed to delete attendance record', {
        description: error instanceof Error ? error.message : undefined,
      })
    }
  }

  const handleMarkAttendance = async () => {
    if (!formData.employee_id) {
      toast.error('Please select an employee')
      return
    }

    setIsSubmitting(true)
    try {
      await markAttendance(formData)
      setIsMarkDialogOpen(false)
      setFormData({
        employee_id: '',
        date: formatDateISO(new Date()),
        status: ATTENDANCE_STATUS.PRESENT,
        notes: '',
      })
      toast.success('Attendance marked successfully')
    } catch (error) {
      toast.error('Failed to mark attendance', {
        description: error instanceof Error ? error.message : undefined,
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case ATTENDANCE_STATUS.PRESENT:
        return <Badge variant="success">Present</Badge>
      case ATTENDANCE_STATUS.ABSENT:
        return <Badge variant="destructive">Absent</Badge>
      case ATTENDANCE_STATUS.HALF_DAY:
        return <Badge variant="warning">Half Day</Badge>
      case ATTENDANCE_STATUS.LEAVE:
        return <Badge variant="secondary">Leave</Badge>
      default:
        return <Badge>{status}</Badge>
    }
  }

  if (loading && records.length === 0) {
    return (
      <div className="flex h-full items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (error && records.length === 0) {
    return <ErrorState message={error} onRetry={() => fetchAttendance()} />
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Attendance</h1>
          <p className="text-muted-foreground">Track employee attendance</p>
        </div>
        <Button onClick={() => setIsMarkDialogOpen(true)}>Mark Attendance</Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Filter Attendance</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <div className="space-y-2">
              <Label>Employee</Label>
              <Select
                value={filters.employee_id}
                onValueChange={(value) => setFilters({ ...filters, employee_id: value })}
              >
                <SelectTrigger>
                  <SelectValue placeholder="All Employees" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Employees</SelectItem>
                  {employees.map((emp) => (
                    <SelectItem key={emp.employee_id} value={emp.employee_id}>
                      {emp.full_name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>Status</Label>
              <Select
                value={filters.status}
                onValueChange={(value) => setFilters({ ...filters, status: value })}
              >
                <SelectTrigger>
                  <SelectValue placeholder="All Statuses" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Statuses</SelectItem>
                  <SelectItem value={ATTENDANCE_STATUS.PRESENT}>Present</SelectItem>
                  <SelectItem value={ATTENDANCE_STATUS.ABSENT}>Absent</SelectItem>
                  <SelectItem value={ATTENDANCE_STATUS.HALF_DAY}>Half Day</SelectItem>
                  <SelectItem value={ATTENDANCE_STATUS.LEAVE}>Leave</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>Start Date</Label>
              <Input
                type="date"
                value={filters.start_date}
                onChange={(e) => setFilters({ ...filters, start_date: e.target.value })}
              />
            </div>
            <div className="space-y-2">
              <Label>End Date</Label>
              <Input
                type="date"
                value={filters.end_date}
                onChange={(e) => setFilters({ ...filters, end_date: e.target.value })}
              />
            </div>
          </div>
          <div className="mt-4 flex gap-2">
            <Button onClick={handleApplyFilters}>Apply Filters</Button>
            <Button variant="outline" onClick={handleClearFilters}>
              Clear
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Attendance Records ({records.length})</CardTitle>
        </CardHeader>
        <CardContent>
          {records.length === 0 ? (
            <EmptyState
              title="No attendance records found"
              description="Start marking attendance for your employees"
              action={{ label: 'Mark Attendance', onClick: () => setIsMarkDialogOpen(true) }}
            />
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Date</TableHead>
                  <TableHead>Employee ID</TableHead>
                  <TableHead>Name</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Notes</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {records.map((record) => (
                  <TableRow key={record.id}>
                    <TableCell className="font-medium">{formatDate(new Date(record.date))}</TableCell>
                    <TableCell>{record.employee_id}</TableCell>
                    <TableCell>{record.employee_name || '-'}</TableCell>
                    <TableCell>{getStatusBadge(record.status)}</TableCell>
                    <TableCell className="max-w-xs truncate">{record.notes || '-'}</TableCell>
                    <TableCell className="text-right">
                      <Button
                        size="sm"
                        variant="destructive"
                        onClick={() => openDeleteDialog(record)}
                      >
                        Delete
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>

      <Dialog open={isMarkDialogOpen} onOpenChange={setIsMarkDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Mark Attendance</DialogTitle>
            <DialogDescription>Record attendance for an employee</DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="employee">Employee</Label>
              <Select
                value={formData.employee_id}
                onValueChange={(value) => setFormData({ ...formData, employee_id: value })}
                disabled={isSubmitting}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select employee" />
                </SelectTrigger>
                <SelectContent>
                  {employees.map((emp) => (
                    <SelectItem key={emp.employee_id} value={emp.employee_id}>
                      {emp.full_name} ({emp.employee_id})
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="date">Date</Label>
              <Input
                id="date"
                type="date"
                value={formData.date}
                max={formatDateISO(new Date())}
                onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                disabled={isSubmitting}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="status">Status</Label>
              <Select
                value={formData.status}
                onValueChange={(value) => setFormData({ ...formData, status: value })}
                disabled={isSubmitting}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value={ATTENDANCE_STATUS.PRESENT}>Present</SelectItem>
                  <SelectItem value={ATTENDANCE_STATUS.ABSENT}>Absent</SelectItem>
                  <SelectItem value={ATTENDANCE_STATUS.HALF_DAY}>Half Day</SelectItem>
                  <SelectItem value={ATTENDANCE_STATUS.LEAVE}>Leave</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="notes">Notes (Optional)</Label>
              <Input
                id="notes"
                value={formData.notes}
                onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                placeholder="Add any notes..."
                disabled={isSubmitting}
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsMarkDialogOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleMarkAttendance} disabled={isSubmitting}>
              {isSubmitting ? 'Marking...' : 'Mark Attendance'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        open={isDeleteDialogOpen}
        onOpenChange={setIsDeleteDialogOpen}
        title="Delete Attendance Record"
        description={`Are you sure you want to delete this attendance record? This action cannot be undone.`}
        onConfirm={handleDeleteAttendance}
        confirmLabel="Delete"
        variant="destructive"
      />
    </div>
  )
}
