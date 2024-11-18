import React from 'react';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useJobsData } from '../../hooks/dataJobs';

const JobFilters = () => {
  const { filters, handleFilterChange } = useJobsData();

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <Input
        placeholder="Filtrar por empresa"
        value={filters.company}
        onChange={(e) => handleFilterChange('company', e.target.value)}
        className="w-full"
      />
      <Input
        placeholder="Filtrar por ubicación"
        value={filters.location}
        onChange={(e) => handleFilterChange('location', e.target.value)}
        className="w-full"
      />
      <Select
        value={filters.datePosted}
        onValueChange={(value) => handleFilterChange('datePosted', value)}
      >
        <SelectTrigger>
          <SelectValue placeholder="Fecha de publicación" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="today">Hoy</SelectItem>
          <SelectItem value="week">Última semana</SelectItem>
          <SelectItem value="month">Último mes</SelectItem>
        </SelectContent>
      </Select>
    </div>
  );
};

export default JobFilters;
