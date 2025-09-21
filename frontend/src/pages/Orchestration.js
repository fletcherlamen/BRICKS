import React, { useState } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Play, 
  Pause, 
  Square, 
  Brain, 
  Network, 
  Zap,
  Settings,
  Plus,
  Activity,
  Target
} from 'lucide-react';

const OrchestrationContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const PageHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
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

const ActionButtons = styled.div`
  display: flex;
  gap: 1rem;
`;

const Button = styled(motion.button)`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;

  &.primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
    }
  }

  &.secondary {
    background: white;
    color: #4a5568;
    border: 2px solid #e2e8f0;

    &:hover {
      border-color: #667eea;
      color: #667eea;
      transform: translateY(-2px);
    }
  }
`;

const ContentGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
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

const SessionForm = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const Label = styled.label`
  font-weight: 600;
  color: #4a5568;
`;

const Input = styled.input`
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s ease;

  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
`;

const TextArea = styled.textarea`
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  min-height: 120px;
  resize: vertical;
  transition: all 0.2s ease;

  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
`;

const AISystemGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
`;

const AISystemCard = styled(motion.div)`
  background: ${props => props.status === 'active' ? '#f0f9ff' : '#f8fafc'};
  border: 2px solid ${props => props.status === 'active' ? '#3b82f6' : '#e2e8f0'};
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  }
`;

const AISystemIcon = styled.div`
  width: 48px;
  height: 48px;
  background: ${props => props.bg || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'};
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin: 0 auto 1rem;
`;

const AISystemName = styled.h4`
  font-size: 1rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 0.5rem 0;
`;

const AISystemStatus = styled.div`
  font-size: 0.875rem;
  color: ${props => {
    switch (props.status) {
      case 'active': return '#3b82f6';
      case 'healthy': return '#48bb78';
      case 'degraded': return '#ed8936';
      case 'down': return '#f56565';
      default: return '#64748b';
    }
  }};
  font-weight: 500;
`;

const SessionList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const SessionCard = styled(motion.div)`
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.2s ease;

  &:hover {
    background: #f0f9ff;
    border-color: #3b82f6;
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  }
`;

const SessionHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
`;

const SessionTitle = styled.h4`
  font-size: 1.125rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0;
`;

const SessionStatus = styled.span`
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;

  &.active {
    background: #dbeafe;
    color: #1d4ed8;
  }

  &.completed {
    background: #dcfce7;
    color: #166534;
  }

  &.failed {
    background: #fee2e2;
    color: #dc2626;
  }
`;

const SessionDetails = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
  color: #64748b;
`;

const SessionActions = styled.div`
  display: flex;
  gap: 0.5rem;
`;

const ControlButton = styled.button`
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;

  &.play {
    background: #48bb78;
    color: white;

    &:hover {
      background: #38a169;
    }
  }

  &.pause {
    background: #ed8936;
    color: white;

    &:hover {
      background: #dd6b20;
    }
  }

  &.stop {
    background: #f56565;
    color: white;

    &:hover {
      background: #e53e3e;
    }
  }
`;

const aiSystems = [
  {
    id: 'crewai',
    name: 'CrewAI',
    status: 'active',
    icon: Brain,
    bg: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  },
  {
    id: 'mem0',
    name: 'Mem0.ai',
    status: 'healthy',
    icon: Zap,
    bg: 'linear-gradient(135deg, #48bb78 0%, #38a169 100%)'
  },
  {
    id: 'orchestrator',
    name: 'Orchestrator',
    status: 'active',
    icon: Network,
    bg: 'linear-gradient(135deg, #ed8936 0%, #dd6b20 100%)'
  },
  {
    id: 'strategic',
    name: 'Strategic AI',
    status: 'healthy',
    icon: Target,
    bg: 'linear-gradient(135deg, #9f7aea 0%, #805ad5 100%)'
  }
];

const mockSessions = [
  {
    id: '1',
    name: 'BRICKS Strategic Analysis',
    status: 'active',
    created: '2 minutes ago',
    collaborations: 12
  },
  {
    id: '2',
    name: 'Revenue Opportunity Mapping',
    status: 'completed',
    created: '1 hour ago',
    collaborations: 8
  },
  {
    id: '3',
    name: 'Church Kit Integration',
    status: 'active',
    created: '3 hours ago',
    collaborations: 15
  }
];

function Orchestration() {
  const [newSession, setNewSession] = useState({
    name: '',
    description: '',
    analysisType: 'strategic'
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Starting new session:', newSession);
    // TODO: Implement session creation
  };

  const handleSystemToggle = (systemId) => {
    console.log('Toggling system:', systemId);
    // TODO: Implement system toggle
  };

  return (
    <OrchestrationContainer>
      <PageHeader>
        <div>
          <PageTitle>Orchestration Control</PageTitle>
          <PageSubtitle>Coordinate AI systems for strategic BRICKS development</PageSubtitle>
        </div>
        <ActionButtons>
          <Button
            className="secondary"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <Settings size={20} />
            Configure
          </Button>
          <Button
            className="primary"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <Plus size={20} />
            New Session
          </Button>
        </ActionButtons>
      </PageHeader>

      <ContentGrid>
        <Section>
          <SectionHeader>
            <SectionTitle>
              <Play size={24} />
              Start New Session
            </SectionTitle>
          </SectionHeader>
          <SessionForm onSubmit={handleSubmit}>
            <FormGroup>
              <Label>Session Name</Label>
              <Input
                type="text"
                placeholder="e.g., BRICKS Strategic Analysis"
                value={newSession.name}
                onChange={(e) => setNewSession({ ...newSession, name: e.target.value })}
              />
            </FormGroup>
            <FormGroup>
              <Label>Description</Label>
              <TextArea
                placeholder="Describe the strategic objective and context..."
                value={newSession.description}
                onChange={(e) => setNewSession({ ...newSession, description: e.target.value })}
              />
            </FormGroup>
            <FormGroup>
              <Label>Analysis Type</Label>
              <Input
                type="text"
                placeholder="strategic, revenue, gap_detection"
                value={newSession.analysisType}
                onChange={(e) => setNewSession({ ...newSession, analysisType: e.target.value })}
              />
            </FormGroup>
            <Button
              type="submit"
              className="primary"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <Play size={20} />
              Start Orchestration
            </Button>
          </SessionForm>
        </Section>

        <Section>
          <SectionHeader>
            <SectionTitle>
              <Network size={24} />
              AI Systems
            </SectionTitle>
          </SectionHeader>
          <AISystemGrid>
            {aiSystems.map((system, index) => {
              const Icon = system.icon;
              return (
                <AISystemCard
                  key={system.id}
                  status={system.status}
                  onClick={() => handleSystemToggle(system.id)}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <AISystemIcon bg={system.bg}>
                    <Icon size={24} />
                  </AISystemIcon>
                  <AISystemName>{system.name}</AISystemName>
                  <AISystemStatus status={system.status}>
                    {system.status.charAt(0).toUpperCase() + system.status.slice(1)}
                  </AISystemStatus>
                </AISystemCard>
              );
            })}
          </AISystemGrid>
        </Section>
      </ContentGrid>

      <Section>
        <SectionHeader>
          <SectionTitle>
            <Activity size={24} />
            Active Sessions
          </SectionTitle>
        </SectionHeader>
        <SessionList>
          <AnimatePresence>
            {mockSessions.map((session, index) => (
              <SessionCard
                key={session.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
              >
                <SessionHeader>
                  <SessionTitle>{session.name}</SessionTitle>
                  <SessionStatus className={session.status}>
                    {session.status}
                  </SessionStatus>
                </SessionHeader>
                <SessionDetails>
                  <div>
                    <strong>{session.collaborations}</strong> AI collaborations
                  </div>
                  <div>Started {session.created}</div>
                </SessionDetails>
                <SessionActions style={{ marginTop: '1rem' }}>
                  <ControlButton className="play" title="Resume">
                    <Play size={16} />
                  </ControlButton>
                  <ControlButton className="pause" title="Pause">
                    <Pause size={16} />
                  </ControlButton>
                  <ControlButton className="stop" title="Stop">
                    <Square size={16} />
                  </ControlButton>
                </SessionActions>
              </SessionCard>
            ))}
          </AnimatePresence>
        </SessionList>
      </Section>
    </OrchestrationContainer>
  );
}

export default Orchestration;
