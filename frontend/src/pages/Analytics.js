import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { 
  BarChart3, 
  TrendingUp, 
  Activity, 
  Brain,
  Zap,
  DollarSign,
  Clock,
  Target
} from 'lucide-react';

const AnalyticsContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const PageHeader = styled.div`
  margin-bottom: 1rem;
`;

const PageTitle = styled.h1`
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
`;

const PageSubtitle = styled.p`
  font-size: 1.125rem;
  color: #64748b;
  margin: 0.5rem 0 0 0;
`;

const MetricsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
`;

const MetricCard = styled(motion.div)`
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

const MetricHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
`;

const MetricIcon = styled.div`
  width: 48px;
  height: 48px;
  background: ${props => props.bg || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'};
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
`;

const MetricValue = styled.div`
  font-size: 2.5rem;
  font-weight: 800;
  color: #1a202c;
  margin-bottom: 0.5rem;
`;

const MetricLabel = styled.div`
  font-size: 1rem;
  font-weight: 600;
  color: #4a5568;
  margin-bottom: 0.25rem;
`;

const MetricChange = styled.div`
  font-size: 0.875rem;
  color: ${props => props.positive ? '#48bb78' : '#f56565'};
  display: flex;
  align-items: center;
  gap: 0.25rem;
`;

const ChartsGrid = styled.div`
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
`;

const ChartSection = styled.div`
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
`;

const ChartHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
`;

const ChartTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
`;

const ChartPlaceholder = styled.div`
  height: 300px;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  font-size: 1.125rem;
  font-weight: 600;
`;

const RevenueList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const RevenueItem = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 12px;
  border-left: 4px solid #48bb78;
`;

const RevenueInfo = styled.div`
  flex: 1;
`;

const RevenueName = styled.div`
  font-weight: 600;
  color: #1a202c;
  margin-bottom: 0.25rem;
`;

const RevenueDescription = styled.div`
  font-size: 0.875rem;
  color: #64748b;
`;

const RevenueAmount = styled.div`
  font-size: 1.25rem;
  font-weight: 700;
  color: #48bb78;
`;

const CollaborationLog = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-height: 400px;
  overflow-y: auto;
`;

const LogItem = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 12px;
  border-left: 4px solid #667eea;
`;

const LogIcon = styled.div`
  width: 40px;
  height: 40px;
  background: #667eea;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
`;

const LogContent = styled.div`
  flex: 1;
`;

const LogTitle = styled.div`
  font-weight: 600;
  color: #1a202c;
  margin-bottom: 0.25rem;
`;

const LogTime = styled.div`
  font-size: 0.875rem;
  color: #64748b;
`;

const SystemPerformance = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
`;

const PerformanceCard = styled.div`
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 12px;
  text-align: center;
  border: 2px solid ${props => props.status === 'healthy' ? '#48bb78' : '#f56565'};
`;

const PerformanceName = styled.h4`
  font-size: 1rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 0.5rem 0;
`;

const PerformanceValue = styled.div`
  font-size: 2rem;
  font-weight: 800;
  color: ${props => props.status === 'healthy' ? '#48bb78' : '#f56565'};
  margin-bottom: 0.5rem;
`;

const PerformanceLabel = styled.div`
  font-size: 0.875rem;
  color: #64748b;
`;

const metrics = [
  {
    icon: Activity,
    value: '24',
    label: 'Sessions Today',
    change: '+12%',
    positive: true,
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  },
  {
    icon: Brain,
    value: '156',
    label: 'AI Collaborations',
    change: '+8%',
    positive: true,
    gradient: 'linear-gradient(135deg, #48bb78 0%, #38a169 100%)'
  },
  {
    icon: DollarSign,
    value: '$12.5K',
    label: 'Revenue Opportunities',
    change: '+15%',
    positive: true,
    gradient: 'linear-gradient(135deg, #9f7aea 0%, #805ad5 100%)'
  },
  {
    icon: Clock,
    value: '2.3s',
    label: 'Avg Response Time',
    change: '-5%',
    positive: true,
    gradient: 'linear-gradient(135deg, #ed8936 0%, #dd6b20 100%)'
  }
];

const revenueOpportunities = [
  {
    name: 'Church Kit Generator Integration',
    description: 'Automated legal formation services',
    amount: '$15,000'
  },
  {
    name: 'Global Sky AI Optimization',
    description: 'Performance-based business optimization',
    amount: '$8,500'
  },
  {
    name: 'Dream Big Masks Automation',
    description: 'E-commerce automation enhancement',
    amount: '$5,200'
  },
  {
    name: 'Treasury Management System',
    description: 'Yield optimization improvements',
    amount: '$12,000'
  }
];

const collaborationLogs = [
  {
    icon: Brain,
    title: 'CrewAI → Strategic Analyst',
    description: 'Strategic analysis completed for BRICKS roadmap',
    time: '2 minutes ago'
  },
  {
    icon: Zap,
    title: 'Mem0.ai → Orchestrator',
    description: 'Context memory updated with strategic insights',
    time: '5 minutes ago'
  },
  {
    icon: Target,
    title: 'Revenue Optimizer → CrewAI',
    description: 'Revenue opportunity analysis requested',
    time: '12 minutes ago'
  },
  {
    icon: Brain,
    title: 'CrewAI → Mem0.ai',
    description: 'Strategic context shared for persistence',
    time: '18 minutes ago'
  }
];

const systemPerformance = [
  { name: 'CrewAI', value: '99.2%', status: 'healthy' },
  { name: 'Mem0.ai', value: '98.7%', status: 'healthy' },
  { name: 'Orchestrator', value: '99.8%', status: 'healthy' },
  { name: 'Database', value: '99.5%', status: 'healthy' }
];

function Analytics() {
  return (
    <AnalyticsContainer>
      <PageHeader>
        <PageTitle>Analytics Dashboard</PageTitle>
        <PageSubtitle>Monitor AI collaboration performance and strategic insights</PageSubtitle>
      </PageHeader>

      <MetricsGrid>
        {metrics.map((metric, index) => {
          const Icon = metric.icon;
          return (
            <MetricCard
              key={index}
              gradient={metric.gradient}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <MetricHeader>
                <MetricIcon bg={metric.gradient}>
                  <Icon size={24} />
                </MetricIcon>
              </MetricHeader>
              <MetricValue>{metric.value}</MetricValue>
              <MetricLabel>{metric.label}</MetricLabel>
              <MetricChange positive={metric.positive}>
                <TrendingUp size={16} />
                {metric.change} from last week
              </MetricChange>
            </MetricCard>
          );
        })}
      </MetricsGrid>

      <ChartsGrid>
        <ChartSection>
          <ChartHeader>
            <ChartTitle>
              <BarChart3 size={24} />
              AI Collaboration Timeline
            </ChartTitle>
          </ChartHeader>
          <ChartPlaceholder>
            📊 Interactive Chart Coming Soon
          </ChartPlaceholder>
        </ChartSection>

        <ChartSection>
          <ChartHeader>
            <ChartTitle>
              <DollarSign size={24} />
              Revenue Opportunities
            </ChartTitle>
          </ChartHeader>
          <RevenueList>
            {revenueOpportunities.map((opportunity, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
              >
                <RevenueItem>
                  <RevenueInfo>
                    <RevenueName>{opportunity.name}</RevenueName>
                    <RevenueDescription>{opportunity.description}</RevenueDescription>
                  </RevenueInfo>
                  <RevenueAmount>{opportunity.amount}</RevenueAmount>
                </RevenueItem>
              </motion.div>
            ))}
          </RevenueList>
        </ChartSection>
      </ChartsGrid>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
        <ChartSection>
          <ChartHeader>
            <ChartTitle>
              <Activity size={24} />
              Recent Collaborations
            </ChartTitle>
          </ChartHeader>
          <CollaborationLog>
            {collaborationLogs.map((log, index) => {
              const Icon = log.icon;
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                >
                  <LogItem>
                    <LogIcon>
                      <Icon size={20} />
                    </LogIcon>
                    <LogContent>
                      <LogTitle>{log.title}</LogTitle>
                      <LogTime>{log.time}</LogTime>
                    </LogContent>
                  </LogItem>
                </motion.div>
              );
            })}
          </CollaborationLog>
        </ChartSection>

        <ChartSection>
          <ChartHeader>
            <ChartTitle>
              <Target size={24} />
              System Performance
            </ChartTitle>
          </ChartHeader>
          <SystemPerformance>
            {systemPerformance.map((system, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
              >
                <PerformanceCard status={system.status}>
                  <PerformanceName>{system.name}</PerformanceName>
                  <PerformanceValue status={system.status}>{system.value}</PerformanceValue>
                  <PerformanceLabel>Uptime</PerformanceLabel>
                </PerformanceCard>
              </motion.div>
            ))}
          </SystemPerformance>
        </ChartSection>
      </div>
    </AnalyticsContainer>
  );
}

export default Analytics;
