import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { 
  Brain, 
  Network, 
  Activity, 
  TrendingUp,
  Zap,
  Target,
  BarChart3,
  Clock
} from 'lucide-react';

const DashboardContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const DashboardHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
`;

const HeaderTitle = styled.h1`
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
`;

const HeaderSubtitle = styled.p`
  font-size: 1.125rem;
  color: #64748b;
  margin: 0.5rem 0 0 0;
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
`;

const StatCard = styled(motion.div)`
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: ${props => props.gradient || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'};
  }
`;

const StatHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
`;

const StatIcon = styled.div`
  width: 48px;
  height: 48px;
  background: ${props => props.bg || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'};
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
`;

const StatValue = styled.div`
  font-size: 2.5rem;
  font-weight: 800;
  color: #1a202c;
  margin-bottom: 0.5rem;
`;

const StatLabel = styled.div`
  font-size: 1rem;
  font-weight: 600;
  color: #4a5568;
  margin-bottom: 0.25rem;
`;

const StatChange = styled.div`
  font-size: 0.875rem;
  color: ${props => props.positive ? '#48bb78' : '#f56565'};
  display: flex;
  align-items: center;
  gap: 0.25rem;
`;

const ContentGrid = styled.div`
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
`;

const MainContent = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const Section = styled.div`
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
`;

const SectionHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
`;

const SectionTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
`;

const ActivityList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const ActivityItem = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 12px;
  border-left: 4px solid #667eea;
`;

const ActivityIcon = styled.div`
  width: 40px;
  height: 40px;
  background: #667eea;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
`;

const ActivityContent = styled.div`
  flex: 1;
`;

const ActivityTitle = styled.div`
  font-weight: 600;
  color: #1a202c;
  margin-bottom: 0.25rem;
`;

const ActivityTime = styled.div`
  font-size: 0.875rem;
  color: #64748b;
`;

const Sidebar = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const QuickActions = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const ActionButton = styled(motion.button)`
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  color: #4a5568;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    border-color: #667eea;
    color: #667eea;
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.15);
  }
`;

const SystemStatus = styled.div`
  .status-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 0;
    border-bottom: 1px solid #e2e8f0;

    &:last-child {
      border-bottom: none;
    }
  }

  .status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #48bb78;
    animation: pulse 2s infinite;
  }
`;

const stats = [
  {
    icon: Brain,
    value: '3',
    label: 'Active Sessions',
    change: '+12%',
    positive: true,
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  },
  {
    icon: Network,
    value: '24',
    label: 'AI Collaborations',
    change: '+8%',
    positive: true,
    gradient: 'linear-gradient(135deg, #48bb78 0%, #38a169 100%)'
  },
  {
    icon: Activity,
    value: '156',
    label: 'Tasks Completed',
    change: '+23%',
    positive: true,
    gradient: 'linear-gradient(135deg, #ed8936 0%, #dd6b20 100%)'
  },
  {
    icon: TrendingUp,
    value: '$12.5K',
    label: 'Revenue Opportunities',
    change: '+15%',
    positive: true,
    gradient: 'linear-gradient(135deg, #9f7aea 0%, #805ad5 100%)'
  }
];

const recentActivity = [
  {
    icon: Brain,
    title: 'Strategic Analysis Completed',
    description: 'BRICKS roadmap analysis for Q1 2024',
    time: '2 minutes ago'
  },
  {
    icon: Network,
    title: 'CrewAI Collaboration',
    description: 'Multi-agent coordination session started',
    time: '15 minutes ago'
  },
  {
    icon: Zap,
    title: 'Mem0.ai Memory Updated',
    description: 'Strategic context persisted successfully',
    time: '32 minutes ago'
  },
  {
    icon: Target,
    title: 'Revenue Opportunity Identified',
    description: 'Church Kit Generator integration potential',
    time: '1 hour ago'
  }
];

const systemStatusData = [
  { name: 'CrewAI', status: 'healthy' },
  { name: 'Mem0.ai', status: 'healthy' },
  { name: 'Database', status: 'healthy' },
  { name: 'API Gateway', status: 'healthy' }
];

function Dashboard() {
  return (
    <DashboardContainer>
      <DashboardHeader>
        <div>
          <HeaderTitle>Dashboard</HeaderTitle>
          <HeaderSubtitle>I PROACTIVE BRICK Orchestration Intelligence</HeaderSubtitle>
        </div>
      </DashboardHeader>

      <StatsGrid>
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <StatCard
              key={index}
              gradient={stat.gradient}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <StatHeader>
                <StatIcon bg={stat.gradient}>
                  <Icon size={24} />
                </StatIcon>
              </StatHeader>
              <StatValue>{stat.value}</StatValue>
              <StatLabel>{stat.label}</StatLabel>
              <StatChange positive={stat.positive}>
                <TrendingUp size={16} />
                {stat.change} from last week
              </StatChange>
            </StatCard>
          );
        })}
      </StatsGrid>

      <ContentGrid>
        <MainContent>
          <Section>
            <SectionHeader>
              <SectionTitle>
                <Activity size={24} />
                Recent Activity
              </SectionTitle>
            </SectionHeader>
            <ActivityList>
              {recentActivity.map((activity, index) => {
                const Icon = activity.icon;
                return (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.5, delay: index * 0.1 }}
                  >
                    <ActivityItem>
                      <ActivityIcon>
                        <Icon size={20} />
                      </ActivityIcon>
                      <ActivityContent>
                        <ActivityTitle>{activity.title}</ActivityTitle>
                        <ActivityTime>{activity.time}</ActivityTime>
                      </ActivityContent>
                    </ActivityItem>
                  </motion.div>
                );
              })}
            </ActivityList>
          </Section>
        </MainContent>

        <Sidebar>
          <Section>
            <SectionHeader>
              <SectionTitle>
                <Zap size={24} />
                Quick Actions
              </SectionTitle>
            </SectionHeader>
            <QuickActions>
              <ActionButton
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <Brain size={20} />
                Start New Session
              </ActionButton>
              <ActionButton
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <Target size={20} />
                Strategic Analysis
              </ActionButton>
              <ActionButton
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <BarChart3 size={20} />
                View Analytics
              </ActionButton>
            </QuickActions>
          </Section>

          <Section>
            <SectionHeader>
              <SectionTitle>
                <Clock size={24} />
                System Status
              </SectionTitle>
            </SectionHeader>
            <SystemStatus>
              {systemStatusData.map((item, index) => (
                <div key={index} className="status-item">
                  <span>{item.name}</span>
                  <div className="status-dot" />
                </div>
              ))}
            </SystemStatus>
          </Section>
        </Sidebar>
      </ContentGrid>
    </DashboardContainer>
  );
}

export default Dashboard;
