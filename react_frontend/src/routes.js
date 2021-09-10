import { Navigate, useRoutes } from 'react-router-dom';
// layouts
import DashboardLayout from './layouts/dashboard';

//
import DashboardApp from './pages/DashboardApp';
import DashboardAppContact from './pages/DashboardAppContact';
import DashboardAppExplainability from './pages/DashboardAppExplainability';
import DashboardAppInference from './pages/DashboardAppInference';
import DashboardAppDrift from './pages/DashboardAppDrift';
import Products from './pages/Products';
import NotFound from './pages/Page404';
import About from './pages/About';

// ----------------------------------------------------------------------

export default function Router() {
  return useRoutes([
    {
      path: '/dashboard',
      element: <DashboardLayout />,
      children: [
        { path: '/', element: <Navigate to="/dashboard/catalog/" replace /> },
        { path: 'app/info/:id', element: <DashboardApp /> },
        { path: 'app/inference/:id', element: <DashboardAppInference /> },
        { path: 'app/explainability/:id', element: <DashboardAppExplainability /> },
        { path: 'app/drift/:id', element: <DashboardAppDrift /> },
        { path: 'catalog', element: <Products /> },
        { path: 'app/contact/:id', element: <DashboardAppContact /> }
      ]
    },
    {
      path: '/',
      element: <DashboardLayout />,
      children: [
        { path: '404', element: <NotFound /> },
        { path: '/about', element: <About /> }
      ]
    },

    { path: '*', element: <Navigate to="/404" replace /> }
  ]);
}
