import csv
import os
from typing import List, Dict, Any
from datetime import datetime

class CSVUtils:
    """
    Utility class for creating CSV files from candidate scores.
    """
    @staticmethod
    def create_csv(data: List[Dict[str, Any]]) -> str:
        """
        Creates a CSV file from a list of dictionaries containing candidate scores.
        
        Args:
            data: List of dictionaries with candidate_name and scores
                 Example: [
                    {
                        'candidate_name': 'Rajkumar T',
                        'scores': [
                            {'criteria': 'required_skills', 'score': 2},
                            {'criteria': 'preferred_skills', 'score': 4},
                            ...
                        ]
                    },
                    ...
                 ]
        
        Returns:
            str: Path to the created CSV file
        """
        if not data:
            return ""
        
        # Create a directory for storing CSV files if it doesn't exist
        output_dir = "output_files"
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate a unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"{output_dir}/resume_scores_{timestamp}.csv"
        
        # Extract all unique criteria from the data
        all_criteria = set()
        for candidate in data:
            for score_item in candidate.get('scores', []):
                all_criteria.add(score_item['criteria'])
        
        all_criteria = sorted(list(all_criteria))
        
        # Write data to CSV
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = ['Candidate Name'] + all_criteria + ['Total Score']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for candidate in data:
                row = {'Candidate Name': candidate.get('candidate_name', 'Unknown')}
                
                # Initialize scores for all criteria to 0
                for criteria in all_criteria:
                    row[criteria] = 0
                
                # Fill in the actual scores
                total_score = 0
                for score_item in candidate.get('scores', []):
                    criteria = score_item['criteria']
                    score = score_item['score']
                    row[criteria] = score
                    total_score += score
                
                row['Total Score'] = total_score
                writer.writerow(row)
        
        return csv_filename
