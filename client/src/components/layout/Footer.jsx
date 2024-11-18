import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="bg-white border-t">
      <div className="container mx-auto px-4 py-6">
        <div className="flex justify-between items-center">
          <p className="text-gray-600">© 2024 JobScraper. Todos los derechos reservados.</p>
          <div className="space-x-4">
            <Link to="/" className="text-gray-600 hover:text-blue-600">
              Inicio
            </Link>
            <Link to="/dashboard" className="text-gray-600 hover:text-blue-600">
              Dashboard
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;