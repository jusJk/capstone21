import { Icon } from '@iconify/react';
import pieChart2Fill from '@iconify/icons-eva/pie-chart-2-fill';
import fileTextFill from '@iconify/icons-eva/file-text-fill';
import lockFill from '@iconify/icons-eva/email-fill';
import browserFill from '@iconify/icons-eva/cloud-upload-fill';
import activityFill from '@iconify/icons-eva/activity-fill';
import React from 'react';

// ----------------------------------------------------------------------

const getIcon = (name) => <Icon icon={name} width={22} height={22} />;

const sidebarConfig = [
  {
    title: 'Model Information',
    path: '/dashboard/app/info',
    icon: getIcon(fileTextFill)
  },
  {
    title: 'Inference',
    path: '/dashboard/app/inference/',
    icon: getIcon(browserFill)
  },

  {
    title: 'Explainability',
    path: '/dashboard/app/explainability',
    icon: getIcon(pieChart2Fill)
  },
  {
    title: 'Model Performance',
    path: '/dashboard/app/performance',
    icon: getIcon(activityFill)
  },
  {
    title: 'Contact',
    path: '/dashboard/app/contact',
    icon: getIcon(lockFill)
  }
];

export const sidebarConfigProvider = (admin) =>
  admin
    ? [
        ...sidebarConfig,
        { title: 'Model Admin', path: '/dashboard/app/admin', icon: getIcon(activityFill) }
      ]
    : sidebarConfig;
