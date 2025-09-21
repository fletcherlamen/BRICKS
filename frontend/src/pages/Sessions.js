import React, { useState } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Activity, 
  Play, 
  Pause, 
  Square, 
  Eye,
  Download,
  Filter,
  Search,
  Clock,
  Brain,
  Network
} from 'lucide-react';

const SessionsContainer = styled.div`
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

const Controls = styled.div`
  display: flex;
  gap: 1rem;
  align-items: center;
`;

const SearchBox = styled.div`
  position: relative;
  display: flex;
  align-items: center;
`;

const SearchInput = styled.input`
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  width: 300px;
  transition: all 0.2s ease;

  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
`;

const SearchIcon = styled(Search)`
  position: absolute;
  left: 0.75rem;
  color: #64748b;
  width: 20px;
  height: 20px;
`;

const FilterButton = styled.button`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  color: #4a5568;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    border-color: #667eea;
    color: #667eea;
  }
`;

const SessionsList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const SessionCard = styled(motion.div)`
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 2rem;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;

  &:hover {
    border-color: #667eea;
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.15);
  }

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: ${props => {
      switch (props.status) {
        case 'active': return 'linear-gradient(135deg, #48bb78 0%, #38a169 100%)';
        case 'completed': return 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        case 'failed': return 'linear-gradient(135deg, #f56565 0%, #e53e3e 100%)';
        default: return 'linear-gradient(135deg, #64748b 0%, #4a5568 100%)';
      }
    }};
  }
`;

const SessionHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
`;

const SessionTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 700;
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
    background: #dcfce7;
    color: #166534;
  }

  &.completed {
    background: #dbeafe;
    color: #1d4ed8;
  }

  &.failed {
    background: #fee2e2;
    color: #dc2626;
  }

  &.paused {
    background: #fef3c7;
    color: #92400e;
  }
`;

const SessionDetails = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
`;

const DetailItem = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: #f8fafc;
  border-radius: 8px;
`;

const DetailIcon = styled.div`
  width: 32px;
  height: 32px;
  background: #667eea;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
`;

const DetailContent = styled.div`
  flex: 1;
`;

const DetailLabel = styled.div`
  font-size: 0.75rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
`;

const DetailValue = styled.div`
  font-size: 0.875rem;
  font-weight: 600;
  color: #1a202c;
`;

const SessionActions = styled.div`
  display: flex;
  gap: 0.75rem;
  align-items: center;
`;

const ActionButton = styled(motion.button)`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;

  &.primary {
    background: #667eea;
    color: white;

    &:hover {
      background: #5a67d8;
      transform: translateY(-1px);
    }
  }

  &.secondary {
    background: white;
    color: #4a5568;
    border: 2px solid #e2e8f0;

    &:hover {
      border-color: #667eea;
      color: #667eea;
    }
  }

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

const ControlButton = styled.button`
  width: 40px;
  height: 40px;
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

const mockSessions = [
  {
    id: '1',
    name: 'BRICKS Strategic Analysis Q1 2024',
    status: 'active',
    created: '2024-01-15T10:30:00Z',
    duration: '2h 15m',
    collaborations: 24,
    agents: ['Strategic Analyst', 'Revenue Optimizer'],
    progress: 75
  },
  {
    id: '2',
    name: 'Church Kit Generator Integration',
    status: 'completed',
    created: '2024-01-15T08:00:00Z',
    duration: '4h 32m',
    collaborations: 18,
    agents: ['Technical Implementer', 'Strategic Analyst'],
    progress: 100
  },
  {
    id: '3',
    name: 'Revenue Opportunity Mapping',
    status: 'paused',
    created: '2024-01-14T16:45:00Z',
    duration: '1h 20m',
    collaborations: 12,
    agents: ['Revenue Optimizer', 'Strategic Analyst'],
    progress: 45
  },
  {
    id: '4',
    name: 'Global Sky AI Performance Analysis',
    status: 'failed',
    created: '2024-01-14T14:20:00Z',
    duration: '0h 15m',
    collaborations: 3,
    agents: ['Technical Implementer'],
    progress: 10
  }
];

function Sessions() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState('all');

  const filteredSessions = mockSessions.filter(session => {
    const matchesSearch = session.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filter === 'all' || session.status === filter;
    return matchesSearch && matchesFilter;
  });

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  const handleSessionAction = (sessionId, action) => {
    console.log(`${action} session ${sessionId}`);
    // TODO: Implement session actions
  };

  return (
    <SessionsContainer>
      <PageHeader>
        <div>
          <PageTitle>Orchestration Sessions</PageTitle>
          <PageSubtitle>Monitor and manage AI collaboration sessions</PageSubtitle>
        </div>
        <Controls>
          <SearchBox>
            <SearchIcon />
            <SearchInput
              type="text"
              placeholder="Search sessions..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </SearchBox>
          <FilterButton onClick={() => setFilter(filter === 'all' ? 'active' : 'all')}>
            <Filter size={20} />
            {filter === 'all' ? 'All Sessions' : 'Active Only'}
          </FilterButton>
        </Controls>
      </PageHeader>

      <SessionsList>
        <AnimatePresence>
          {filteredSessions.map((session, index) => (
            <SessionCard
              key={session.id}
              status={session.status}
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
                <DetailItem>
                  <DetailIcon>
                    <Clock size={16} />
                  </DetailIcon>
                  <DetailContent>
                    <DetailLabel>Created</DetailLabel>
                    <DetailValue>{formatDate(session.created)}</DetailValue>
                  </DetailContent>
                </DetailItem>

                <DetailItem>
                  <DetailIcon>
                    <Activity size={16} />
                  </DetailIcon>
                  <DetailContent>
                    <DetailLabel>Duration</DetailLabel>
                    <DetailValue>{session.duration}</DetailValue>
                  </DetailContent>
                </DetailItem>

                <DetailItem>
                  <DetailIcon>
                    <Network size={16} />
                  </DetailIcon>
                  <DetailContent>
                    <DetailLabel>Collaborations</DetailLabel>
                    <DetailValue>{session.collaborations}</DetailValue>
                  </DetailContent>
                </DetailItem>

                <DetailItem>
                  <DetailIcon>
                    <Brain size={16} />
                  </DetailIcon>
                  <DetailContent>
                    <DetailLabel>Agents</DetailLabel>
                    <DetailValue>{session.agents.length}</DetailValue>
                  </DetailContent>
                </DetailItem>
              </SessionDetails>

              <SessionActions>
                {session.status === 'active' && (
                  <>
                    <ControlButton
                      className="pause"
                      onClick={() => handleSessionAction(session.id, 'pause')}
                      title="Pause Session"
                    >
                      <Pause size={20} />
                    </ControlButton>
                    <ControlButton
                      className="stop"
                      onClick={() => handleSessionAction(session.id, 'stop')}
                      title="Stop Session"
                    >
                      <Square size={20} />
                    </ControlButton>
                  </>
                )}

                {session.status === 'paused' && (
                  <ControlButton
                    className="play"
                    onClick={() => handleSessionAction(session.id, 'resume')}
                    title="Resume Session"
                  >
                    <Play size={20} />
                  </ControlButton>
                )}

                <ActionButton
                  className="primary"
                  onClick={() => handleSessionAction(session.id, 'view')}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <Eye size={18} />
                  View Details
                </ActionButton>

                <ActionButton
                  className="secondary"
                  onClick={() => handleSessionAction(session.id, 'download')}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <Download size={18} />
                  Export
                </ActionButton>
              </SessionActions>
            </SessionCard>
          ))}
        </AnimatePresence>
      </SessionsList>
    </SessionsContainer>
  );
}

export default Sessions;
