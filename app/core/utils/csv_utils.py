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
            # Convert criteria to title case for the header
            title_case_criteria = [criteria.replace('_', ' ').title() for criteria in all_criteria]
            fieldnames = ['Candidate Name'] + title_case_criteria + ['Total Score']
            
            # Create a mapping from original criteria to title case criteria
            criteria_mapping = {orig: title for orig, title in zip(all_criteria, title_case_criteria)}
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for candidate in data:
                row = {'Candidate Name': candidate.get('candidate_name', 'Unknown')}
                
                # Initialize scores for all criteria to 0
                for criteria, title_criteria in criteria_mapping.items():
                    row[title_criteria] = 0
                
                # Fill in the actual scores
                total_score = 0
                max_possible_score = 0
                for score_item in candidate.get('scores', []):
                    criteria = score_item['criteria']
                    title_criteria = criteria_mapping[criteria]
                    score = score_item['score']
                    row[title_criteria] = score
                    total_score += score
                    # Assuming each criteria has a maximum score of 5
                    max_possible_score += 5
                
                # Format total score as score/total
                row['Total Score'] = f"{total_score}/{max_possible_score}"
                writer.writerow(row)
        
        return csv_filename
