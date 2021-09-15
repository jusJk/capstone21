import PropTypes from 'prop-types';

// material
import { alpha, styled } from '@material-ui/core/styles';
import { Box, Stack, AppBar, Toolbar, IconButton, Button } from '@material-ui/core';
import { useEffect } from 'react';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import Typography from '@material-ui/core/Typography';
import shoppingBagFill from '@iconify/icons-eva/shopping-bag-fill';

// components
import Logo from '../../components/Logo';

// ----------------------------------------------------------------------

const APPBAR_MOBILE = 64;
const APPBAR_DESKTOP = 92;

const RootStyle = styled(AppBar)(({ theme }) => ({
  boxShadow: '1px',
  backdropFilter: 'blur(6px)',
  WebkitBackdropFilter: 'blur(6px)', // Fix on Mobile
  backgroundColor: alpha(theme.palette.background.default, 0.9),
  zIndex: theme.zIndex.drawer + 1
}));

const ToolbarStyle = styled(Toolbar)(({ theme }) => ({
  minHeight: APPBAR_MOBILE,
  padding: theme.spacing(5, 0),
  [theme.breakpoints.up('lg')]: {
    minHeight: APPBAR_DESKTOP,
    padding: theme.spacing(0, 5)
  }
}));

// ----------------------------------------------------------------------

DashboardNavbar.propTypes = {
  onOpenSidebar: PropTypes.func
};

export default function DashboardNavbar({ onOpenSidebar }) {
  const loc = useLocation();
  console.log();
  return (
    <RootStyle>
      <ToolbarStyle>
        <Box sx={{ px: 1, py: 1 }}>
          <Box component={RouterLink} to="/" sx={{ display: 'inline-flex' }}>
            <Logo />
          </Box>
        </Box>
        <Box sx={{ mr: 5 }}>
          <Typography variant="h4" sx={{ color: 'black' }}>
            <b>AI-aaS</b>
          </Typography>
        </Box>
        <Box component={RouterLink} to="/">
          <Button fullWidth size="large" variant={loc.pathname === '/' ? 'contained' : 'outlined'}>
            <Typography variant="subtitle1">Home</Typography>
          </Button>
        </Box>
        <Box component={RouterLink} to="/dashboard/catalog/" sx={{ px: 1 }}>
          <Button
            fullWidth
            size="large"
            variant={
              loc.pathname === '/dashboard/catalog/' || loc.pathname.includes('dashboard/app')
                ? 'contained'
                : 'outlined'
            }
          >
            <Typography variant="subtitle1">Model Catalog</Typography>
          </Button>
        </Box>
      </ToolbarStyle>
    </RootStyle>
  );
}
