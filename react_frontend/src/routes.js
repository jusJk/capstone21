import { Navigate, useRoutes } from 'react-router-dom';
import React, { useState } from 'react';
import DashboardLayout from './layouts/dashboard';
import BasicLayout from './layouts/basic';
import DashboardApp from './pages/DashboardApp';
import DashboardAppContact from './pages/DashboardAppContact';
import DashboardAppExplainability from './pages/DashboardAppExplainability';
import DashboardAppInference from './pages/DashboardAppInference';
import DashboardAppPerformance from './pages/DashboardAppPerformance';
import DashboardAppAdmin from './pages/DashboardAppAdmin';
import Products from './pages/Products';
import NotFound from './pages/Page404';
import Landing from './pages/Landing';

// ----------------------------------------------------------------------

export default function Router() {
  const [userProfile, setUserProfile] = useState('Admin');
  return useRoutes([
    {
      path: '/dashboard',
      element: <DashboardLayout userProfile={userProfile} setUserProfile={setUserProfile} />,
      children: [
        { path: '/', element: <Navigate to="/dashboard/catalog/" replace /> },
        { path: 'app/info/:id', element: <DashboardApp /> },
        { path: 'app/inference/:id', element: <DashboardAppInference /> },
        { path: 'app/explainability/:id', element: <DashboardAppExplainability /> },
        { path: 'app/admin/:id', element: <DashboardAppAdmin userProfile={userProfile} /> },
        { path: 'app/performance/:id', element: <DashboardAppPerformance /> },
        { path: 'app/contact/:id', element: <DashboardAppContact /> }
      ]
    },

    {
      path: '/',
      element: <BasicLayout userProfile={userProfile} setUserProfile={setUserProfile} />,
      children: [
        { path: '404', element: <NotFound /> },
        { path: 'catalog', element: <Products /> },
        {
          path: '/',
          element: <Landing setUserProfile={setUserProfile} userProfile={userProfile} />
        }
      ]
    },

    { path: '*', element: <Navigate to="/404" replace /> }
  ]);
}
