import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import JobFilters from '../components/dashboard/JobFilters';
import JobsTable from '../components/dashboard/JobsTable';
import { useJobsData } from '../hooks/dataJobs';

const Dashboard = () => {
  const { jobs, loading, filters, handleFilterChange } = useJobsData();

  return (
    <div className="container mx-auto px-4 py-8">
      <Card>
        <CardHeader>
          <CardTitle>Búsqueda de Empleos</CardTitle>
        </CardHeader>
        <CardContent>
          <JobFilters filters={filters} onFilterChange={handleFilterChange} />
          <JobsTable jobs={jobs} loading={loading} />
        </CardContent>
      </Card>
    </div>
  );
};

export default Dashboard;
