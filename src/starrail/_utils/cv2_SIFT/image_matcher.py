# SPDX-License-Identifier: MIT
# MIT License
#
# Copyright (c) 2023 Kevin L.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import cv2
import numpy as np

class StarRailImageMatcher:
    def __init__(self):
        pass

    def match_image(self, template, screenshot, show_match=False):
        """
        SIFT (Scale Invariant Feature Transform) algorithm for feature detection and description, and FLANN (Fast Library for Approximate Nearest Neighbors) for feature matching. 
        The algorithm also uses RANSAC for finding homography to account for any scale, rotation or translation between the images.
        
        :param template: absolute path to the template image
        :param screenshot: absolute path to the screenshot image
        :show_match: generate a visualization for the match. Defaulted to False for optimization. 
        """
        img1 = cv2.imread(template, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(screenshot, cv2.IMREAD_GRAYSCALE)

        # Initialize SIFT detector
        sift = cv2.SIFT_create()

        # Detect SIFT features in both images
        keypoints1, descriptors1 = sift.detectAndCompute(img1, None)
        keypoints2, descriptors2 = sift.detectAndCompute(img2, None)

        # Initialize FLANN matcher
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)

        # Match features between the template and screenshot
        matches = flann.knnMatch(descriptors1, descriptors2, k=2)

        # Store all good matches as per Lowe's ratio test
        good = []
        for m, n in matches:
            if m.distance < 0.85 * n.distance:
                good.append(m)

        # print(len(good))
        if len(good) >= 100: # 100 works well enough with 0.85 * n.distance
            src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            # Compute Homography with RANSAC
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

            # Apply the Homography to transform the corners of template to find corresponding region in the screenshot
            h, w = img1.shape
            pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)

            # Compute the center of the matched region
            center_x = np.mean(dst[..., 0])
            center_y = np.mean(dst[..., 1])

            img2_with_box = None
            if show_match == True: # Show template match on screenshot
                # Draw a red rectangle around the detected region in screenshot
                img2_color = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)  # Convert to colored image for visualization
                img2_with_box = cv2.polylines(img2_color, [np.int32(dst)], True, (0, 0, 255), 3, cv2.LINE_AA)

            return img2_with_box, M, (center_x, center_y)

        else:
            print("Not enough matches are found - %d/%d" % (len(good), 100))
            return None, None, None

if __name__ == "__main__":
    import os
    image_detector = StarRailImageMatcher()

    TEMPLATE                    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp_data", "template.PNG")
    ORIGINAL                    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp_data", "original.PNG")
    ORIGINAL_2                  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp_data", "original-2.png")
    ORIGINAL_ORIENTED           = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp_data", "original-oriented.jpg")
    ORIGINAL_COMPRESSED         = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp_data", "original-compressed.jpg")
    ORIGINAL_DOUBLE_COMPRESSED  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp_data", "original-double-compressed.jpg")

    SC_with_box, M, center = image_detector.match_image(TEMPLATE, ORIGINAL_DOUBLE_COMPRESSED)

    if M is not None:
        cv2.imshow("visualization with Box", SC_with_box)
        cv2.waitKey(0)
        cv2.destroyAllWindows()