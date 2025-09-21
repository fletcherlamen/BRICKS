import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { 
  Home, 
  Network, 
  BarChart3, 
  Activity,
  Brain,
  Zap,
  Target
} from 'lucide-react';

const SidebarContainer = styled(motion.aside)`
  position: fixed;
  left: 0;
  top: 0;
  width: 280px;
  height: 100vh;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-right: 1px solid rgba(255, 255, 255, 0.2);
  padding: 2rem 0;
  z-index: 1000;
`;

const SidebarHeader = styled.div`
  padding: 0 2rem 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 2rem;
`;

const SidebarTitle = styled.h2`
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
  margin: 0 0 0.5rem 0;
`;

const SidebarSubtitle = styled.p`
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
`;

const Navigation = styled.nav`
  padding: 0 1rem;
`;

const NavGroup = styled.div`
  margin-bottom: 2rem;
`;

const NavGroupTitle = styled.h3`
  font-size: 0.75rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.5);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin: 0 0 1rem 1rem;
`;

const NavItem = styled(motion.button)`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.875rem 1rem;
  margin-bottom: 0.25rem;
  background: ${props => props.active ? 'rgba(255, 255, 255, 0.2)' : 'transparent'};
  border: none;
  border-radius: 12px;
  color: ${props => props.active ? 'white' : 'rgba(255, 255, 255, 0.8)'};
  font-size: 0.875rem;
  font-weight: 500;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;

  &:hover {
    background: rgba(255, 255, 255, 0.15);
    color: white;
    transform: translateX(4px);
  }

  ${props => props.active && `
    &::before {
      content: '';
      position: absolute;
      left: 0;
      top: 50%;
      transform: translateY(-50%);
      width: 3px;
      height: 20px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border-radius: 0 2px 2px 0;
    }
  `}
`;

const NavIcon = styled.div`
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const SystemStatus = styled.div`
  margin-top: auto;
  padding: 1.5rem 2rem 0;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
`;

const StatusTitle = styled.h4`
  font-size: 0.875rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
  margin: 0 0 1rem 0;
`;

const StatusItem = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);

  &:last-child {
    border-bottom: none;
  }
`;

const StatusLabel = styled.span`
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.7);
`;

const StatusValue = styled.span`
  font-size: 0.75rem;
  font-weight: 600;
  color: ${props => {
    switch (props.status) {
      case 'healthy': return '#48bb78';
      case 'degraded': return '#ed8936';
      case 'down': return '#f56565';
      default: return 'rgba(255, 255, 255, 0.7)';
    }
  }};
`;

const navItems = [
  {
    group: 'Core',
    items: [
      { path: '/', label: 'Dashboard', icon: Home },
      { path: '/orchestration', label: 'Orchestration', icon: Network },
      { path: '/sessions', label: 'Sessions', icon: Activity },
      { path: '/analytics', label: 'Analytics', icon: BarChart3 }
    ]
  },
  {
    group: 'AI Systems',
    items: [
      { path: '/crewai', label: 'CrewAI', icon: Brain },
      { path: '/mem0', label: 'Mem0.ai', icon: Zap },
      { path: '/strategic', label: 'Strategic Analysis', icon: Target }
    ]
  }
];

const systemStatus = [
  { label: 'CrewAI', status: 'healthy' },
  { label: 'Mem0.ai', status: 'healthy' },
  { label: 'Orchestrator', status: 'healthy' },
  { label: 'Database', status: 'healthy' }
];

function Sidebar() {
  const location = useLocation();
  const navigate = useNavigate();

  return (
    <SidebarContainer
      initial={{ x: -280 }}
      animate={{ x: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
    >
      <SidebarHeader>
        <SidebarTitle>BRICK Intelligence</SidebarTitle>
        <SidebarSubtitle>Phase 1 - Foundation</SidebarSubtitle>
      </SidebarHeader>

      <Navigation>
        {navItems.map((group, groupIndex) => (
          <NavGroup key={groupIndex}>
            <NavGroupTitle>{group.group}</NavGroupTitle>
            {group.items.map((item, itemIndex) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              
              return (
                <NavItem
                  key={itemIndex}
                  active={isActive}
                  onClick={() => navigate(item.path)}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <NavIcon>
                    <Icon size={18} />
                  </NavIcon>
                  {item.label}
                </NavItem>
              );
            })}
          </NavGroup>
        ))}
      </Navigation>

      <SystemStatus>
        <StatusTitle>System Status</StatusTitle>
        {systemStatus.map((status, index) => (
          <StatusItem key={index}>
            <StatusLabel>{status.label}</StatusLabel>
            <StatusValue status={status.status}>
              {status.status.charAt(0).toUpperCase() + status.status.slice(1)}
            </StatusValue>
          </StatusItem>
        ))}
      </SystemStatus>
    </SidebarContainer>
  );
}

export default Sidebar;
