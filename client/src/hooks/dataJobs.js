import { useState, useEffect, useCallback } from 'react';

export const useJobsData = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    company: '',
    location: '',
    datePosted: ''
  });

  const fetchJobs = useCallback(async () => {
    try {
      const queryParams = new URLSearchParams();
      if (filters.company) queryParams.append('company', filters.company);
      if (filters.location) queryParams.append('location', filters.location);
      if (filters.datePosted) queryParams.append('datePosted', filters.datePosted);
      
      const response = await fetch(`/api/jobs?${queryParams}`);
      const data = await response.json();
      setJobs(data);
    } catch (error) {
      console.error('Error fetching jobs:', error);
    } finally {
      setLoading(false);
    }
  }, [filters]); // Memoizamos la función con filters como dependencia

  useEffect(() => {
    fetchJobs();
  }, [fetchJobs]); // Ahora podemos usar fetchJobs como dependencia

  const handleFilterChange = useCallback((key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  }, []); // También memoizamos handleFilterChange

  return { jobs, loading, filters, handleFilterChange };
};