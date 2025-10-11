#!/usr/bin/env python3
"""
Script to check BRICK proposals in the database directly
"""

import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.database import AsyncSessionLocal
from app.models.strategic import BRICKProposal
from sqlalchemy import select

async def check_proposals():
    """Check proposals in database directly"""
    async with AsyncSessionLocal() as db:
        try:
            # Query all proposals
            result = await db.execute(select(BRICKProposal))
            all_proposals = result.scalars().all()
            
            print(f"Total proposals in database: {len(all_proposals)}")
            
            # Group by brick_name
            brick_name_counts = {}
            for proposal in all_proposals:
                brick_name = proposal.brick_name
                if brick_name not in brick_name_counts:
                    brick_name_counts[brick_name] = []
                brick_name_counts[brick_name].append(proposal)
            
            print("Brick name distribution:")
            for brick_name, proposals in brick_name_counts.items():
                print(f"  {brick_name}: {len(proposals)} proposals")
                for i, proposal in enumerate(proposals):
                    print(f"    {i+1}. ID: {proposal.proposal_id}, Created: {proposal.created_at}")
            
        except Exception as e:
            print(f"❌ Error checking proposals: {str(e)}")
            raise

async def main():
    """Main function"""
    print("🔍 Checking BRICK proposals in database...")
    
    try:
        await check_proposals()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(main())
