import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { styled } from '@material-ui/core/styles';
import { Box, Drawer, Typography, Button } from '@material-ui/core';

import Scrollbar from '../../components/Scrollbar';
import NavSection from '../../components/NavSection';
import { MHidden } from '../../components/@material-extend';
//
import { sidebarConfigProvider } from './SidebarConfig';

// ----------------------------------------------------------------------

const DRAWER_WIDTH = 280;

const RootStyle = styled('div')(({ theme }) => ({
  [theme.breakpoints.up('lg')]: {
    flexShrink: 0,
    width: DRAWER_WIDTH
  }
}));

const AccountStyle = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: theme.spacing(2, 2.5),
  borderRadius: theme.shape.borderRadiusSm,
  backgroundColor: theme.palette.grey[200]
}));

// ----------------------------------------------------------------------

export default function DashboardSidebar({ userProfile, ...rest }) {
  const loc = useLocation();
  const id = loc.pathname.split('/').slice(-1)[0];

  const renderContent = (
    <Scrollbar
      sx={{
        height: '100%',
        '& .simplebar-content': { height: '100%', display: 'flex', flexDirection: 'column' }
      }}
    >
      <Box sx={{ mt: 15, mb: 5 }}>
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'row',
            justifyContent: 'center',
            padding: 0
          }}
        >
          <Button component={Link} to="/catalog/" variant="secondary">
            {'<  '}Back to Model Catalog
          </Button>
        </Box>

        <AccountStyle sx={{ mt: 3, mx: 2.5 }}>
          {/* <Avatar src={account.photoURL} alt="photoURL" /> */}
          <Box sx={{ ml: 2 }}>
            Model
            <Typography variant="h5" sx={{ color: 'text.primary' }}>
              <b>{id}</b>
            </Typography>
          </Box>
        </AccountStyle>
      </Box>

      <NavSection navConfig={sidebarConfigProvider(userProfile === 'Admin')} id={id} />
      <Box sx={{ flexGrow: 1 }} />
    </Scrollbar>
  );

  return (
    <RootStyle>
      <MHidden width="lgUp">
        <Drawer
          PaperProps={{
            sx: { width: DRAWER_WIDTH }
          }}
        >
          {renderContent}
        </Drawer>
      </MHidden>

      <MHidden width="lgDown">
        <Drawer
          open
          variant="persistent"
          PaperProps={{
            sx: {
              width: DRAWER_WIDTH,
              bgcolor: 'background.default'
            }
          }}
        >
          {renderContent}
        </Drawer>
      </MHidden>
    </RootStyle>
  );
}
