class ParallelSimulator:
    def run(self, designs):
        results = []

        for design in designs:
            score = 0.0

            if "routing" in design:
                score += 0.8
            if "memory" in design:
                score += 0.7
            if "cluster" in design:
                score += 0.9
            if "stability" in design:
                score += 1.0

            results.append({
                "design": design,
                "score": score
            })

        return results
