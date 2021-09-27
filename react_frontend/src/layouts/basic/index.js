import { Outlet } from 'react-router-dom';
import React from 'react';
import { styled } from '@material-ui/core/styles';
import DashboardNavbar from './DashboardNavbar';

// ----------------------------------------------------------------------

const APP_BAR_MOBILE = 64;
const APP_BAR_DESKTOP = 92;

const RootStyle = styled('div')({
  display: 'flex',
  minHeight: '100%',
  overflow: 'hidden'
});

const MainStyle = styled('div')(({ theme }) => ({
  flexGrow: 1,
  overflow: 'auto',
  minHeight: '100%',
  paddingTop: APP_BAR_MOBILE + 24,
  paddingBottom: theme.spacing(10),
  [theme.breakpoints.up('lg')]: {
    paddingTop: APP_BAR_DESKTOP + 24,
    paddingLeft: theme.spacing(2),
    paddingRight: theme.spacing(2)
  }
}));

// ----------------------------------------------------------------------

export default function BasicLayout({ userProfile, setUserProfile }) {
  return (
    <RootStyle>
      <DashboardNavbar userProfile={userProfile} setUserProfile={setUserProfile} />
      <MainStyle>
        <Outlet />
      </MainStyle>
    </RootStyle>
  );
}
