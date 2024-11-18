import React from 'react';
import PropTypes from 'prop-types';

const JobsTable = ({ jobs = [], loading = false }) => {
  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse">
        <thead>
          <tr className="bg-gray-50">
            <th className="p-4 text-left border">Título</th>
            <th className="p-4 text-left border">Empresa</th>
            <th className="p-4 text-left border">Ubicación</th>
            <th className="p-4 text-left border">Plataforma</th>
            <th className="p-4 text-left border">Fecha</th>
            <th className="p-4 text-left border">Acciones</th>
          </tr>
        </thead>
        <tbody>
          {loading ? (
            <tr>
              <td colSpan="6" className="text-center p-4">Cargando...</td>
            </tr>
          ) : jobs.map((job, index) => (
            <tr key={index} className="hover:bg-gray-50">
              <td className="p-4 border">{job.title}</td>
              <td className="p-4 border">{job.company}</td>
              <td className="p-4 border">{job.location}</td>
              <td className="p-4 border">{job.platform}</td>
              <td className="p-4 border">{new Date(job.date_posted).toLocaleDateString()}</td>
              <td className="p-4 border">
                <a
                  href={job.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800"
                >
                  Ver oferta
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

JobsTable.propTypes = {
  jobs: PropTypes.arrayOf(
    PropTypes.shape({
      title: PropTypes.string.isRequired,
      company: PropTypes.string.isRequired,
      location: PropTypes.string.isRequired,
      platform: PropTypes.string.isRequired,
      date_posted: PropTypes.string.isRequired,
      link: PropTypes.string.isRequired
    })
  ),
  loading: PropTypes.bool
};

JobsTable.defaultProps = {
  jobs: [],
  loading: false
};

export default JobsTable;