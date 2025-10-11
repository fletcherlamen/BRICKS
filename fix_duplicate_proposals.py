#!/usr/bin/env python3
"""
Script to fix duplicate BRICK proposals in the database
"""

import asyncio
import sys
import os
from datetime import datetime, timezone

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.database import AsyncSessionLocal
from app.models.strategic import BRICKProposal
from sqlalchemy import text, select, func

async def fix_duplicate_proposals():
    """Remove duplicate proposals and keep only unique ones"""
    async with AsyncSessionLocal() as db:
        try:
            # First, let's see what we have
            result = await db.execute(select(BRICKProposal))
            all_proposals = result.scalars().all()
            
            print(f"Total proposals in database: {len(all_proposals)}")
            
            # Group by brick_name to find duplicates
            brick_name_counts = {}
            for proposal in all_proposals:
                brick_name = proposal.brick_name
                if brick_name not in brick_name_counts:
                    brick_name_counts[brick_name] = []
                brick_name_counts[brick_name].append(proposal)
            
            print("Brick name distribution:")
            for brick_name, proposals in brick_name_counts.items():
                print(f"  {brick_name}: {len(proposals)} proposals")
            
            # Remove duplicates, keeping the most recent one for each brick_name
            duplicates_removed = 0
            for brick_name, proposals in brick_name_counts.items():
                if len(proposals) > 1:
                    # Sort by created_at (most recent first)
                    proposals.sort(key=lambda x: x.created_at, reverse=True)
                    
                    # Keep the first (most recent), remove the rest
                    to_remove = proposals[1:]
                    for proposal in to_remove:
                        await db.delete(proposal)
                        duplicates_removed += 1
                    
                    print(f"Removed {len(to_remove)} duplicate proposals for '{brick_name}'")
            
            await db.commit()
            print(f"✅ Removed {duplicates_removed} duplicate proposals")
            
            # Verify the fix
            result = await db.execute(select(BRICKProposal))
            remaining_proposals = result.scalars().all()
            print(f"Remaining proposals: {len(remaining_proposals)}")
            
            # Show final distribution
            final_counts = {}
            for proposal in remaining_proposals:
                brick_name = proposal.brick_name
                final_counts[brick_name] = final_counts.get(brick_name, 0) + 1
            
            print("Final brick name distribution:")
            for brick_name, count in final_counts.items():
                print(f"  {brick_name}: {count} proposal(s)")
            
        except Exception as e:
            await db.rollback()
            print(f"❌ Error fixing duplicates: {str(e)}")
            raise

async def main():
    """Main function to fix duplicate proposals"""
    print("🔧 Fixing duplicate BRICK proposals...")
    
    try:
        await fix_duplicate_proposals()
        print("🎉 Duplicate proposals fixed successfully!")
        
    except Exception as e:
        print(f"❌ Error during fix: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(main())
