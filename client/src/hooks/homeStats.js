import { useState, useEffect } from 'react';

export const useHomeStats = () => {
  const [stats, setStats] = useState({
    totalJobs: 0,
    linkedinJobs: 0,
    infojobsJobs: 0,
    recentJobs: 0,
    uniqueCompanies: 0
  });

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await fetch('/api/jobs');
      const jobs = await response.json();
      
      const platformCounts = jobs.reduce((acc, job) => {
        acc[job.platform] = (acc[job.platform] || 0) + 1;
        return acc;
      }, {});

      const uniqueCompanies = new Set(jobs.map(job => job.company)).size;
      const recentJobs = jobs.filter(job => {
        const jobDate = new Date(job.date_posted);
        const weekAgo = new Date();
        weekAgo.setDate(weekAgo.getDate() - 7);
        return jobDate >= weekAgo;
      }).length;

      setStats({
        totalJobs: jobs.length,
        linkedinJobs: platformCounts['LinkedIn'] || 0,
        infojobsJobs: platformCounts['InfoJobs'] || 0,
        recentJobs,
        uniqueCompanies
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const chartData = [
    { platform: 'LinkedIn', jobs: stats.linkedinJobs },
    { platform: 'InfoJobs', jobs: stats.infojobsJobs }
  ];

  return { stats, chartData };
};